from typing import Any, Tuple, List, Dict

from torch import nn, Tensor
from torch.nn import functional
import torch

from sihl.layers import ConvNormAct

from .instance_segmentation import InstanceSegmentation


class KeypointDetection(InstanceSegmentation):
    """Keypoint detection is like object detection, except instances are all of the same
    category (i.e. `num_classes` = 1), and are associated with a set of 2D (key)points
    instead of an axis-aligned bounding box. Each instance predictions must provide a 2D
    coordinate for every keypoint, as well as whether each keypoint is present in the
    image or not (i.e. missing or invisible). Coordinate predictions of non-present
    keypoints are safe to ignore.

    References:
        1. [FCPose](https://arxiv.org/abs/2105.14185)
        2. [CondInst](https://arxiv.org/abs/2102.03026)
    """

    def __init__(
        self,
        in_channels: List[int],
        num_keypoints: int,
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
            num_keypoints (int): Number of keypoints.
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
            num_classes=1,
            in_channels=in_channels,
            num_channels=num_channels,
            num_layers=num_layers,
            bottom_level=bottom_level,
            top_level=top_level,
            max_instances=max_instances,
            t_min=t_min,
            t_max=t_max,
            topk=topk,
            soft_label_decay_steps=soft_label_decay_steps,
            top_mask_level=top_mask_level,
        )

        self.num_keypoints = num_keypoints
        self.keypoint_threshold = 0.1  # FIXME: make adaptive
        self.get_masks = self.get_keypoints
        self.bottom_module = ConvNormAct(in_channels[bottom_level], 32)
        controller_out_channels = 2176 + 32 * self.num_keypoints + self.num_keypoints
        self.controller_head = nn.Conv2d(self.num_channels, controller_out_channels, 1)
        # self.refinement_module = nn.Conv2d(
        #     in_channels[bottom_level], 2 * self.num_keypoints, kernel_size=3, stride=1
        # )

        self.output_shapes = {
            "num_instances": ("batch_size",),
            "scores": ("batch_size", self.max_instances),
            "keypoint_scores": ("batch_size", self.max_instances),
            "keypoints": ("batch_size", self.max_instances, self.num_keypoints),
        }

    def forward(self, inputs: List[Tensor]) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
        img_height, img_width = inputs[0].shape[2:]
        # discard irrelevant inputs
        inputs = [inputs[level] for level in self.levels]

        # compute features
        scores, reg_features = self.get_features(inputs)
        scores = scores.max(dim=2)[0]

        # keep only the top `max_instances`
        batch_size = scores.shape[0]
        batches = torch.arange(batch_size).unsqueeze(-1).repeat(1, self.max_instances)
        instance_idxs = scores.topk(self.max_instances).indices
        scores = scores[batches, instance_idxs]
        num_instances = (scores > self.threshold).sum(dim=1)

        # compute segmentation masks for the `max_instances` top scoring anchors
        controllers = self.get_controllers(reg_features)
        bottom_feats = self.get_bottom_features(inputs)
        anchors = self.get_anchors(inputs, normalized=True)

        pred_heatmaps = torch.stack(
            [
                self.get_keypoints(
                    conts[idxs], anchors[idxs], feats, num_masks=self.max_instances
                )
                for idxs, conts, feats in zip(instance_idxs, controllers, bottom_feats)
            ]
        )  # shape: (batch_size, num_instances, num_keypoints, height, width)
        heatmap_height, heatmap_width = pred_heatmaps.shape[3:]
        kpt_scores, kpt_indices = pred_heatmaps.flatten(3, 4).sigmoid().max(dim=3)
        # kpt_scores, kpt_indices = pred_heatmaps.flatten(3, 4).softmax(dim=3).max(dim=3)
        y = kpt_indices / heatmap_width / heatmap_height * img_height
        x = kpt_indices % heatmap_width / heatmap_width * img_width
        pred_keypoints = torch.stack([x, y], dim=-1)
        # offsets = self.refinement_module(bottom_feats).flatten(3, 4).permute(0, 2, 1)
        # offsets = offsets[kpt_indices].reshape((batch_size, -1, self.num_keypoints, 2))
        # pred_keypoints = pred_keypoints + offsets

        return num_instances, scores, kpt_scores, pred_keypoints

    def get_saliency(self, inputs: List[Tensor]) -> Tensor:
        img_height, img_width = inputs[0].shape[2:]
        # discard irrelevant inputs
        inputs = [inputs[level] for level in self.levels]

        # compute features
        scores, reg_features = self.get_features(inputs)
        scores = scores.max(dim=2)[0]

        # keep only the top `max_instances`
        instance_idxs = scores.topk(self.max_instances).indices

        # compute segmentation masks for the `max_instances` top scoring anchors
        controllers = self.get_controllers(reg_features)
        bottom_feats = self.get_bottom_features(inputs)
        anchors = self.get_anchors(inputs, normalized=True)

        return torch.stack(
            [
                self.get_keypoints(
                    conts[idxs], anchors[idxs], feats, num_masks=self.max_instances
                )
                for idxs, conts, feats in zip(instance_idxs, controllers, bottom_feats)
            ]
        )

    def get_keypoints(
        self, params: Tensor, anchors: Tensor, bottom_features: Tensor, num_masks: int
    ) -> Tensor:
        _, height, width = bottom_features.shape

        w1 = params[:, :1088].reshape(32 * num_masks, 32 + 2, 1, 1)
        b1 = params[:, 1088:1120].reshape(32 * num_masks)
        w2 = params[:, 1120:2144].reshape(32 * num_masks, 32, 1, 1)
        b2 = params[:, 2144:2176].reshape(32 * num_masks)
        w3_idx = 2176 + 32 * self.num_keypoints
        w3 = params[:, 2176:w3_idx].reshape(self.num_keypoints * num_masks, 32, 1, 1)
        b3 = params[:, w3_idx:].reshape(self.num_keypoints * num_masks)
        # Convert absolute coords to relative coords
        padded_anchors = functional.pad(anchors, (32, 0, 0, 0))  # (N, 10)
        x = bottom_features.repeat(num_masks, 1, 1) - padded_anchors.reshape(-1, 1, 1)
        x = functional.conv2d(x.unsqueeze(0), w1, b1, groups=num_masks).relu()
        x = functional.conv2d(x, w2, b2, groups=num_masks).relu()
        x = functional.conv2d(x, w3, b3, groups=num_masks)
        return x.reshape((num_masks, self.num_keypoints, height, width))

    def training_step(
        self,
        inputs: List[Tensor],
        keypoints: List[Tensor],  # [(I, K, 2)]
        presence: List[Tensor],  # [(I, K)]
        is_validating: bool = False,
    ) -> Tuple[Tensor, Dict[str, Any]]:
        batch_size, _, img_height, img_width = inputs[0].shape
        inputs = [inputs[level] for level in self.levels]  # discard irrelevant inputs

        scores, reg_features = self.get_features(inputs)
        controllers = self.get_controllers(reg_features)
        pred_boxes = self.get_boxes(reg_features)
        bottom_feats = self.get_bottom_features(inputs)  # (N, 34, H, W)
        anchors = self.get_anchors(inputs)  # (2, H, W)

        # remove empty instances from targets
        keypoints = [
            sample_keypoints[sample_presence.any(dim=1)]
            for sample_keypoints, sample_presence in zip(keypoints, presence)
        ]
        presence = [
            sample_presence[sample_presence.any(dim=1)] for sample_presence in presence
        ]

        # get gt "boxes" (converted from keypoints) and "classes" (all category 0)
        boxes = [
            keypoints_to_boxes(sample_keypoints, sample_presence)
            for (sample_keypoints, sample_presence) in zip(keypoints, presence)
        ]
        classes = [
            torch.zeros(
                (sample_keypoints.shape[0],), dtype=torch.int64, device=scores.device
            )
            for sample_keypoints in keypoints
        ]

        # get object detection losses
        class_target, box_target, assignment = self.get_targets(
            anchors, scores, pred_boxes, classes, boxes, is_validating
        )
        class_loss, box_loss = self.get_losses(
            scores, pred_boxes, class_target, box_target
        )
        class_loss, box_loss = class_loss.nan_to_num(0), box_loss.nan_to_num(0)

        heatmap_losses = []
        heatmap_height, heatmap_width = bottom_feats.shape[2:]
        for batch_idx in range(batch_size):
            pos_idxs = class_target[batch_idx].max(dim=1)[0] == 1.0
            if keypoints[batch_idx].numel() == 0 or not torch.any(pos_idxs):
                continue

            pred_heatmap = self.get_keypoints(
                params=controllers[batch_idx][pos_idxs],
                anchors=anchors[pos_idxs],
                bottom_features=bottom_feats[batch_idx],
                num_masks=pos_idxs.sum(),
            )
            # (num_instances, num_anchors, num_keypoints)
            pred_heatmap = pred_heatmap.flatten(2, 3).permute(0, 2, 1)

            scaled_keypoints = keypoints[batch_idx].clone()
            scaled_keypoints[..., 0] *= (heatmap_height - 1) / img_height
            scaled_keypoints[..., 1] *= (heatmap_width - 1) / img_width
            scaled_keypoints = scaled_keypoints.round().to(torch.int64)

            target_coord = scaled_keypoints[assignment[batch_idx, pos_idxs]]
            xs = functional.one_hot(target_coord[..., 0], heatmap_height).unsqueeze(2)
            ys = functional.one_hot(target_coord[..., 1], heatmap_width).unsqueeze(3)
            target_heatmap = (xs * ys).to(pred_heatmap.dtype)
            target_heatmap = target_heatmap.flatten(2, 3).permute(0, 2, 1)
            target_presence = presence[batch_idx][assignment[batch_idx, pos_idxs]]
            target_heatmap = target_heatmap * target_presence.unsqueeze(1)
            with torch.autocast(device_type="cuda", enabled=False):
                hm_loss = functional.cross_entropy(
                    pred_heatmap, target_heatmap, label_smoothing=0.1, reduction="none"
                )
                nans = hm_loss.isnan()
                heatmap_losses.append(hm_loss.nan_to_num(0).sum() / (~nans).sum())

        if heatmap_losses:
            heatmap_loss = torch.stack(heatmap_losses).mean()
        else:
            heatmap_loss = torch.zeros_like(class_loss)

        return class_loss + box_loss + heatmap_loss, {
            "class_loss": class_loss,
            "box_loss": box_loss,
            "heatmap_loss": heatmap_loss,
        }

    def validation_step(
        self,
        inputs: List[Tensor],
        keypoints: List[Tensor],  # [(I, K, 2)]
        presence: List[Tensor],  # [(I, K)]
        is_validating: bool = False,
    ) -> Tuple[Tensor, Dict[str, Any]]:
        _, scores, kpt_scores, pred_keypoints = self.forward(inputs)

        boxes = [
            keypoints_to_boxes(sample_keypoints, sample_presence)
            for (sample_keypoints, sample_presence) in zip(keypoints, presence)
        ]

        pred_boxes = torch.stack(
            [
                keypoints_to_boxes(kpts, pres > self.keypoint_threshold)
                for (kpts, pres) in zip(pred_keypoints, kpt_scores)
            ]
        )

        self.map_computer.to(scores.device).update(
            [
                {"scores": s, "labels": torch.zeros_like(s, dtype=int), "boxes": b}
                for s, b in zip(scores, pred_boxes)
            ],
            [
                {
                    "labels": torch.zeros(b.shape[0], dtype=int, device=scores.device),
                    "boxes": b,
                }
                for b in boxes
            ],
        )
        loss, metrics = self.training_step(
            inputs, keypoints, presence, is_validating=True
        )
        self.loss_computer.to(loss.device).update(loss)
        return loss, metrics


def compute_oks(
    preds: Tensor, gts: Tensor, scales: Tensor, sigmas: Tensor, visibility: Tensor
) -> Tensor:
    """
    Compute OKS for batched keypoints predictions and ground truths.

    Parameters:
    preds (Tensor): Predicted keypoints (B, K, 2) where B is batch size and K is number of keypoints.
    gts (Tensor): Ground truth keypoints (B, K, 2).
    scales (Tensor): Scale for each object in the batch (B).
    sigmas (Tensor): Standard deviations for each keypoint (K).
    visibility (Tensor): Visibility of ground truth keypoints (B, K), 1 if visible, 0 otherwise.

    Returns:
    Tensor: OKS scores for each object in the batch (B).
    """
    dists = torch.sum((preds - gts) ** 2, dim=2)  # Shape: (B, K)
    scales = scales.unsqueeze(1)  # Shape: (B, 1)
    exp_terms = torch.exp(-dists / (sigmas**2) * 2 * (scales**2)) * visibility  # (B, K)
    oks_scores = exp_terms.sum(dim=1) / visibility.sum(dim=1)
    return oks_scores


def keypoints_to_boxes(keypoints: Tensor, presence: Tensor) -> Tensor:
    masked_keypoints = keypoints.clone()
    masked_keypoints[~presence] = torch.inf
    xmin = masked_keypoints[:, :, 0].min(dim=1)[0]
    ymin = masked_keypoints[:, :, 1].min(dim=1)[0]
    masked_keypoints[~presence] = -torch.inf
    xmax = masked_keypoints[:, :, 0].max(dim=1)[0]
    ymax = masked_keypoints[:, :, 1].max(dim=1)[0]
    return torch.stack([xmin, ymin, xmax, ymax], dim=-1)
