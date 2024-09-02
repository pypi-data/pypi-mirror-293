from typing import Any, Tuple, List, Dict

from torch import nn, Tensor
from torch.nn import functional
from torchmetrics import JaccardIndex, Accuracy
from torchvision.ops import masks_to_boxes
import torch

from sihl.layers import ConvNormAct, BilinearScaler
from sihl.utils import interpolate

from .instance_segmentation import InstanceSegmentation


class PanopticSegmentation(InstanceSegmentation):
    """Panoptic segmentation assigns each pixel of the input to a category and an
    instance index, essentially merging instance segmentation and semantic segmentation
    tasks in one (although, in this case, instances cannot overlap).

    Refs:
        1. [CondInst](https://arxiv.org/abs/2102.03026)
    """

    def __init__(
        self,
        in_channels: List[int],
        num_stuff_classes: int,
        num_thing_classes: int,
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
        ignore_index: int = -100,
    ) -> None:
        """
        Args:
            in_channels (List[int]): Number of channels in input feature maps, sorted by level.
            num_stuff_classes (int): Number of possible stuff categories.
            num_thing_classes (int): Number of possible thing categories.
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
        super().__init__(
            in_channels=in_channels,
            num_classes=num_thing_classes,
            top_mask_level=top_mask_level,
            soft_label_decay_steps=soft_label_decay_steps,
            num_channels=num_channels,
            num_layers=num_layers,
            bottom_level=bottom_level,
            top_level=top_level,
            max_instances=max_instances,
            t_min=t_min,
            t_max=t_max,
            topk=topk,
        )

        self.ignore_index = ignore_index  # https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html
        self.num_stuff_classes = num_stuff_classes
        self.num_thing_classes = num_thing_classes
        self.semantic_branch = nn.ModuleList(
            [ConvNormAct(in_channels[bottom_level], self.num_channels)]
            + [
                nn.Sequential(
                    *[
                        nn.Sequential(
                            ConvNormAct(in_channels[bottom_level], self.num_channels),
                            BilinearScaler(2.0),
                        )
                        for _ in range(level - self.bottom_level)
                    ]
                )
                for level in range(self.bottom_level + 1, self.top_mask_level)
            ]
        )
        self.semantic_out_conv = nn.Conv2d(
            self.num_channels, num_stuff_classes + num_thing_classes, kernel_size=1
        )

        self.output_shapes = {
            "panoptic_maps": (
                "batch_size",
                2,
                f"height/{2**bottom_level}",
                f"width/{2**bottom_level}",
            )
        }

    def get_semantic_map(self, inputs: List[Tensor]) -> Tensor:
        outs = []
        for x, conv in zip(inputs, self.semantic_branch):
            outs.append(conv(x))
        return self.semantic_out_conv(torch.stack(outs).sum(dim=0))

    def forward(self, inputs: List[Tensor]) -> Tensor:
        input_shape = inputs[0].shape[2:]
        inputs = [inputs[level] for level in self.levels]
        scores, reg_features = self.get_features(inputs)
        scores, pred_classes = scores.max(dim=2)
        # keep only the top `max_instances`
        batch_size = scores.shape[0]
        batches = torch.arange(batch_size).unsqueeze(-1).repeat(1, self.max_instances)
        instance_idxs = scores.topk(self.max_instances).indices
        scores = scores[batches, instance_idxs]
        pred_classes = pred_classes[batches, instance_idxs]
        num_instances = (scores > self.threshold).sum(dim=1)
        # compute segmentation masks for the `max_instances` top scoring anchors
        controllers = self.get_controllers(reg_features)
        bottom_features = self.get_bottom_features(inputs)
        anchors = self.get_anchors(inputs)
        instance_masks = [
            self.get_masks(conts[idxs], anchors[idxs], feats, self.max_instances)
            for idxs, conts, feats in zip(instance_idxs, controllers, bottom_features)
        ]
        instance_masks = torch.cat(instance_masks)
        semantic_map = torch.max(
            interpolate(self.get_semantic_map(inputs), size=input_shape), dim=1
        ).indices
        id_map = torch.zeros_like(semantic_map)
        for batch_idx in range(batch_size):
            current_id = 0
            for category in semantic_map[batch_idx].unique():  # FIXME
                id_map[batch_idx][semantic_map[batch_idx] == category] = current_id
                current_id += 1
            score_map = torch.zeros_like(semantic_map[batch_idx], dtype=scores.dtype)
            for instance_idx in range(num_instances[batch_idx]):
                score = scores[batch_idx, instance_idx]
                instance_mask = instance_masks[batch_idx, instance_idx]
                instance_mask = interpolate(
                    instance_mask[None, None, ...], size=input_shape
                )[0, 0]
                category = pred_classes[batch_idx, instance_idx]
                mask = (instance_mask > 0.5) & (score_map < score)
                semantic_map[batch_idx][mask] = category + self.num_stuff_classes
                id_map[batch_idx][mask] = current_id
                score_map[mask] = score  # update scores
                current_id += 1

        panoptic_map = torch.stack([semantic_map, id_map], dim=1)
        # TODO: make non-overlap by taking max score. instance id is argmax index.abs
        # "stuff" map as background. stuff_id = max_thing_id + stuff_class_idx
        return panoptic_map

    def get_instance_masks(self, targets: Tensor) -> Tuple[List[Tensor], List[Tensor]]:
        instance_masks = []
        instance_classes = []
        for target in targets:
            semantic_map, id_map = target
            sample_instance_masks = []
            sample_instance_classes = []
            for segment_id in id_map.unique():
                instance_mask = id_map == segment_id
                category_idx = semantic_map[instance_mask][0]
                if category_idx == self.ignore_index:
                    continue
                if category_idx < self.num_stuff_classes:  # ignore stuff segments
                    continue
                sample_instance_masks.append(instance_mask.to(torch.float))
                sample_instance_classes.append(category_idx - self.num_stuff_classes)
            if len(sample_instance_masks):
                instance_masks.append(torch.stack(sample_instance_masks))
                instance_classes.append(torch.stack(sample_instance_classes))
            else:
                instance_masks.append(torch.empty((0, 1, 1)))
                instance_classes.append(torch.empty((0,)))
        return instance_masks, instance_classes

    def training_step(
        self, inputs: List[Tensor], targets: Tensor
    ) -> Tuple[Tensor, Dict[str, Any]]:
        # targets are concatenated [class_map, id_map]
        # category indices are stuff first, then things, so
        # [0, ..., num_stuff_classes, ..., num_stuff_classes + num_thing_classes]
        instance_masks, instance_classes = self.get_instance_masks(targets)
        instance_loss, instance_metrics = super().training_step(
            inputs, instance_classes, instance_masks
        )
        inputs = [inputs[level] for level in self.levels]
        pred_semantic_map = interpolate(
            self.get_semantic_map(inputs), size=targets.shape[2:]
        )
        semantic_loss = functional.cross_entropy(
            pred_semantic_map,
            targets[:, 0, :, :],
            ignore_index=self.ignore_index,
            reduction="mean",
        )
        loss = instance_loss + semantic_loss
        return loss, instance_metrics

    def on_validation_start(self) -> None:
        super().on_validation_start()
        metric_kwargs = {
            "task": "multiclass",
            "num_classes": self.num_stuff_classes + self.num_thing_classes,
            "ignore_index": self.ignore_index,
        }
        self.pixel_accuracy = Accuracy(**metric_kwargs)
        self.mean_iou_computer = JaccardIndex(**metric_kwargs)

    def validation_step(
        self, inputs: List[Tensor], targets: Tensor
    ) -> Tuple[Tensor, Dict[str, Any]]:
        instance_masks, instance_classes = self.get_instance_masks(targets)
        boxes = [masks_to_boxes(sample_masks) for sample_masks in instance_masks]
        # num_instances, scores, pred_classes, pred_masks = self.forward(inputs)
        scores, reg_features = self.get_features(
            [inputs[level] for level in self.levels]
        )
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
            [{"labels": c, "boxes": b} for c, b in zip(instance_classes, boxes)],
        )
        semantic_targets = targets[:, 0, :, :]
        logits = interpolate(
            self.get_semantic_map([inputs[level] for level in self.levels]),
            size=semantic_targets.shape[1:],
        )
        loss = functional.cross_entropy(
            logits, semantic_targets, ignore_index=self.ignore_index
        )
        scores = logits.sigmoid()
        self.mean_iou_computer.to(loss.device).update(scores, semantic_targets)
        self.pixel_accuracy.to(loss.device).update(scores, semantic_targets)
        return self.training_step(inputs, targets)

    def on_validation_end(self) -> Dict[str, float]:
        metrics = super().on_validation_end()
        metrics["pixel_accuracy"] = self.pixel_accuracy.compute().item()
        metrics["mean_iou"] = self.mean_iou_computer.compute().item()
        return metrics
