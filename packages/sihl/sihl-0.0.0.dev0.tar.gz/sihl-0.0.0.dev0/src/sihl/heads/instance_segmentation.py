from typing import Any, Tuple, List, Dict

from torch import nn, Tensor
from torch.nn import functional
from torchvision.ops import masks_to_boxes
import torch

from sihl.layers import ConvNormAct
from sihl.utils import coordinate_grid, interpolate

from .object_detection import ObjectDetection


class InstanceSegmentation(ObjectDetection):
    """Instance segmentation is like object detection except instances are associated
    with a binary mask instead of a bounding box.

    Refs:
        1. [One-to-Few Label Assignment for End-to-End Dense Detection](https://arxiv.org/abs/2303.11567)
        2. [CondInst](https://arxiv.org/abs/2102.03026)
    """

    def __init__(
        self,
        in_channels: List[int],
        num_classes: int,
        bottom_level: int = 3,
        top_level: int = 7,
        num_channels: int = 256,
        num_layers: int = 4,
        max_instances: int = 100,
        t_min: float = 0.2,
        t_max: float = 0.6,
        topk: int = 7,
        soft_label_decay_steps: int = 1,
        top_mask_level: int = 5,
    ) -> None:
        """
        Args:
            in_channels (List[int]): Number of channels in input feature maps, sorted by level.
            num_classes (int): Number of possible object categories.
            bottom_level (int, optional): Bottom level of inputs this head is attached to. Defaults to 3.
            top_level (int, optional): Top level of inputs this head is attached to. Defaults to 7.
            num_channels (int, optional): Number of convolutional channels. Defaults to 256.
            num_layers (int, optional): Number of convolutional layers. Defaults to 4.
            max_instances (int, optional): Maximum number of instances to predict in a sample. Defaults to 100.
            t_min (float, optional): Lower bound of O2F parameter t. Defaults to 0.2.
            t_max (float, optional): Upper bound of O2F parameter t. Defaults to 0.6.
            topk (int, optional): How many anchors to match to each ground truth object when copmuting the loss. Defaults to 7.
            soft_label_decay_steps (int, optional): How many training steps to perform before the one-to-few matching becomes one-to-one. Defaults to 1.
            top_mask_level (int, optional): Top level of inputs masks are computed from. Defaults to 5.
        """
        assert top_level >= top_mask_level >= bottom_level
        super().__init__(
            in_channels=in_channels,
            num_classes=num_classes,
            bottom_level=bottom_level,
            top_level=top_level,
            num_channels=num_channels,
            num_layers=num_layers,
            max_instances=max_instances,
            t_min=t_min,
            t_max=t_max,
            topk=topk,
            soft_label_decay_steps=soft_label_decay_steps,
        )

        self.top_mask_level = top_mask_level
        self.controller_head = nn.Conv2d(num_channels, 169, kernel_size=1)
        self.bottom_module = ConvNormAct(in_channels[bottom_level], 8)

        self.output_shapes = {
            "num_instances": ("batch_size",),
            "scores": ("batch_size", self.max_instances),
            "classes": ("batch_size", self.max_instances),
            "masks": (
                "batch_size",
                self.max_instances,
                f"height/{2**bottom_level}",
                f"width/{2**bottom_level}",
            ),
        }

    def forward(self, inputs: List[Tensor]) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
        batch_size, _, height, width = inputs[0].shape
        inputs = [inputs[level] for level in self.levels]
        scores, reg_features = self.get_features(inputs)
        scores, pred_classes = scores.max(dim=2)
        # keep only the top `max_instances`
        batches = torch.arange(batch_size).unsqueeze(-1).repeat(1, self.max_instances)
        instance_idxs = scores.topk(self.max_instances).indices
        scores = scores[batches, instance_idxs]
        pred_classes = pred_classes[batches, instance_idxs]
        num_instances = (scores > self.threshold).sum(dim=1)
        # compute segmentation masks for the `max_instances` top scoring anchors
        controllers = self.get_controllers(reg_features)
        bottom_feats = self.get_bottom_features(inputs)
        normed_anchors = self.get_anchors(inputs, normalized=True)
        pred_masks = torch.cat(
            [
                self.get_masks(
                    params=controllers[batch_idx, instance_idxs[batch_idx]],
                    anchors=normed_anchors[instance_idxs[batch_idx]],
                    bottom_features=bottom_feats[batch_idx],
                    num_masks=self.max_instances,
                )
                for batch_idx in range(batch_size)
            ]
        )
        pred_masks = interpolate(pred_masks, size=(height, width))
        return num_instances, scores, pred_classes, pred_masks

    def get_controllers(self, features: Tensor) -> Tensor:
        return torch.cat(
            [self.controller_head(_).flatten(2, 3).transpose(1, 2) for _ in features],
            dim=1,
        )

    def get_bottom_features(self, inputs: List[Tensor]) -> Tensor:
        mask_shape = inputs[0].shape[2:]
        summed_features = torch.stack(
            [inputs[0]]
            + [
                interpolate(inputs[level], size=mask_shape)
                for level in range(1, self.top_mask_level - self.bottom_level + 1)
            ]
        ).sum(dim=0)
        bottom_feats = self.bottom_module(summed_features)  # (N, 8, H, W)
        # Absolute coordinates will later be transformed into relative ones
        abs_coords = coordinate_grid(mask_shape[0], mask_shape[1], 1, 1) * 2 - 1
        abs_coords = abs_coords.unsqueeze(0).expand(bottom_feats.shape[0], -1, -1, -1)
        return torch.cat([bottom_feats, abs_coords.to(bottom_feats)], dim=1)

    def get_masks(
        self, params: Tensor, anchors: Tensor, bottom_features: Tensor, num_masks: int
    ) -> Tensor:
        _, mask_height, mask_width = bottom_features.shape
        w1 = params[:, :80].reshape(8 * num_masks, 10, 1, 1)  # channels: 10 -> 8
        b1 = params[:, 80:88].reshape(8 * num_masks)
        w2 = params[:, 88:152].reshape(8 * num_masks, 8, 1, 1)  # channels: 8 -> 8
        b2 = params[:, 152:160].reshape(8 * num_masks)
        w3 = params[:, 160:168].reshape(num_masks, 8, 1, 1)  # channels: 8 -> 1
        b3 = params[:, 168:169].reshape(num_masks)
        # Convert abs coords to rel coords by subtracting padded anchors
        padded_anchors = functional.pad(anchors, (8, 0, 0, 0))  # (N, 10)
        x = bottom_features.repeat(num_masks, 1, 1) - padded_anchors.reshape(-1, 1, 1)
        x = functional.conv2d(x.unsqueeze(0), w1, b1, groups=num_masks).relu()
        x = functional.conv2d(x, w2, b2, groups=num_masks).relu()
        return functional.conv2d(x, w3, b3, groups=num_masks).sigmoid()

    def training_step(
        self,
        inputs: List[Tensor],
        classes: List[Tensor],
        masks: List[Tensor],
        is_validating: bool = False,
    ) -> Tuple[Tensor, Dict[str, Any]]:
        boxes = [masks_to_boxes(sample_masks) for sample_masks in masks]
        inputs = [inputs[level] for level in self.levels]
        scores, reg_features = self.get_features(inputs)
        controllers = self.get_controllers(reg_features)
        pred_boxes = self.get_boxes(reg_features)
        bottom_feats = self.get_bottom_features(inputs)
        anchors = self.get_anchors(inputs, normalized=False)
        class_target, box_target, assignment = self.get_targets(
            anchors, scores, pred_boxes, classes, boxes, is_validating
        )
        class_loss, box_loss = self.get_losses(
            scores, pred_boxes, class_target, box_target
        )
        mask_losses = []
        batch_size = scores.shape[0]
        normed_anchors = self.get_anchors(inputs, normalized=True)
        for batch_idx in range(batch_size):
            pos_idxs = class_target[batch_idx].max(dim=1)[0] == 1.0
            if masks[batch_idx].numel() == 0 or not torch.any(pos_idxs):
                continue
            pred_masks = self.get_masks(
                params=controllers[batch_idx, pos_idxs],
                anchors=normed_anchors[pos_idxs],
                bottom_features=bottom_feats[batch_idx],
                num_masks=pos_idxs.sum(),
            )
            target_masks = masks[batch_idx][assignment[batch_idx, pos_idxs]][None, ...]
            mask_shape = (target_masks.shape[2], target_masks.shape[3])  # FIXME
            target_masks = interpolate(target_masks, size=mask_shape).squeeze(0)
            pred_masks = interpolate(pred_masks, size=mask_shape).squeeze(0)
            numerator = (pred_masks * target_masks).sum((1, 2))
            denominator = (pred_masks**2).sum((1, 2)) + (target_masks**2).sum((1, 2))
            mask_losses.append((1 - 2 * numerator / denominator).mean())  # dice loss
        mask_loss = torch.nan_to_num(torch.stack(mask_losses), nan=0).mean()
        return class_loss + box_loss + mask_loss, {
            "class_loss": class_loss,
            "box_loss": box_loss,
            "mask_loss": mask_loss,
        }

    def validation_step(
        self, inputs: List[Tensor], classes: List[Tensor], masks: List[Tensor]
    ) -> Tuple[Tensor, Dict[str, Any]]:
        loss, metrics = self.training_step(inputs, classes, masks, is_validating=True)
        self.loss_computer.to(loss.device).update(loss)
        boxes = [masks_to_boxes(sample_masks) for sample_masks in masks]
        # num_instances, scores, pred_classes, pred_masks = self.forward(inputs)
        inputs = [inputs[level] for level in self.levels]
        scores, reg_features = self.get_features(inputs)
        scores, pred_classes = scores.max(dim=2)
        pred_boxes = self.get_boxes(reg_features)
        # keep only the top `max_instances`
        batch_size = scores.shape[0]
        batches = torch.arange(batch_size).unsqueeze(-1).repeat(1, self.max_instances)
        instance_idxs = scores.topk(self.max_instances).indices
        scores = scores[batches, instance_idxs]
        pred_classes = pred_classes[batches, instance_idxs]
        pred_boxes = pred_boxes[batches, instance_idxs]

        map_computer_preds = []
        # for batch_idx, sample_masks in enumerate(pred_masks):
        for batch_idx, sample_boxes in enumerate(pred_boxes):
            # non_empty_idxs = torch.any(sample_masks > 0.5, dim=(1, 2))
            # sample_boxes = masks_to_boxes(sample_masks[non_empty_idxs] > 0.5)
            map_computer_preds.append(
                {
                    "scores": scores[batch_idx],  # [non_empty_idxs],
                    "labels": pred_classes[batch_idx],  # [non_empty_idxs],
                    "boxes": sample_boxes,
                }
            )
        self.map_computer.to(pred_boxes.device).update(
            map_computer_preds,
            [{"labels": c, "boxes": b} for c, b in zip(classes, boxes)],
        )
        return loss, metrics
