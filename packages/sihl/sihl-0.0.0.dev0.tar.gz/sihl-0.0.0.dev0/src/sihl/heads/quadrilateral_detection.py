from typing import Tuple, List, Dict

from torch import nn, Tensor
from torch.nn import functional
import torch

from sihl.utils import coordinate_grid, polygon_iou

from .object_detection import ObjectDetection


class QuadrilateralDetection(ObjectDetection):
    """Quadrilateral detection is like object detection, expect objects are associated
    with convex quadrilaterals instead of axis-aligned rectangles."""

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
        """
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

        del self.box_head
        self.quad_head = nn.Conv2d(self.num_channels, 8, kernel_size=1)
        self.get_boxes = self.get_quads
        self.box_iou = polygon_iou
        self.inside_box = inside_polygon
        self.box_loss = quad_loss

        self.output_shapes = {
            "num_instances": ("batch_size",),
            "scores": ("batch_size", self.max_instances),
            "classes": ("batch_size", self.max_instances),
            "quadrilaterals": ("batch_size", self.max_instances, 4, 2),
        }

    def get_quads(self, features: List[Tensor]) -> Tensor:
        quads, batch_size = [], features[0].shape[0]
        for level, feats in zip(self.levels, features):
            stride, (h, w) = 2**level, feats.shape[2:]
            biases = coordinate_grid(h, w, h * stride, w * stride).to(feats.device)
            biases = biases.flatten(1, 2).transpose(0, 1).repeat(1, 1, 4)
            level_quads = self.quad_head(feats).flatten(2, 3).transpose(1, 2)
            quads.append(biases + level_quads * stride)
        quads = torch.cat(quads, dim=1).reshape(-1, 4, 2)
        return convexify(quads).reshape(batch_size, -1, 4, 2)

    def training_step(
        self,
        inputs: List[Tensor],
        classes: List[Tensor],
        quads: List[Tensor],
        is_validating: bool = False,
    ) -> Tuple[Tensor, Dict[str, float]]:
        loss, metrics = super().training_step(
            inputs=inputs, classes=classes, boxes=quads, is_validating=is_validating
        )
        metrics["quad_loss"] = metrics["box_loss"]
        del metrics["box_loss"]
        return loss, metrics

    def validation_step(
        self, inputs: List[Tensor], classes: List[Tensor], quads: List[Tensor]
    ) -> Tuple[Tensor, Dict[str, float]]:
        num_instances, scores, pred_classes, pred_quads = self.forward(inputs)
        self.map_computer.to(pred_quads.device).update(
            [
                {"scores": s, "labels": c, "boxes": b}
                for s, c, b in zip(scores, pred_classes, quads_to_boxes(pred_quads))
            ],
            [{"labels": c, "boxes": quads_to_boxes(q)} for c, q in zip(classes, quads)],
        )
        loss, metrics = self.training_step(inputs, classes, quads, is_validating=True)
        self.loss_computer.to(loss.device).update(loss)
        return loss, metrics


def quads_to_boxes(quads):
    x, y = quads[..., 0], quads[..., 1]
    return torch.stack([x.min(-1)[0], y.min(-1)[0], x.max(-1)[0], y.max(-1)[0]], dim=-1)


def line_equation(p1: Tensor, p2: Tensor) -> Tuple[float, float, float]:
    """find (a, b, c) such that ax + by + c = 0"""
    a, b, c = p2[1] - p1[1], p1[0] - p2[0], p2[0] * p1[1] - p1[0] * p2[1]
    return a, b, c


def inside_polygon(points: Tensor, polygon: Tensor) -> Tensor:
    """A point is inside a polygon if it is inside all edges' half-planes.
    N points (N, 2), 1 M-sided polygon (M, 2) -> (N,) bool
    """
    m = polygon.shape[0]
    edges = [line_equation(polygon[i], polygon[(i + 1) % m]) for i in range(m)]
    inside = [a * points[:, 0] + b * points[:, 1] + c >= 0 for (a, b, c) in edges]
    return torch.stack(inside).all(dim=0)


def quad_loss(pred_quads: Tensor, targets: Tensor, reduction: str = "mean") -> Tensor:
    """https://arxiv.org/abs/2103.11636"""
    batch_size = pred_quads.shape[0]
    permutations = []
    for shift in range(4):
        shifted_quad = torch.roll(targets, shifts=-shift, dims=1)
        permutations.append(shifted_quad)
        permutations.append(shifted_quad.flip(dims=(1,)))
    targets = torch.stack(permutations, dim=1).flatten(0, 1)  # (N*8, 4, 2)
    pred_quads = pred_quads.repeat_interleave(8, dim=0)
    loss = functional.smooth_l1_loss(pred_quads, targets, reduction="none").mean((1, 2))
    loss = loss.reshape((batch_size, 8)).min(axis=1)[0]
    return 0.1 * loss.mean()


def uncross(quadrilaterals: Tensor) -> Tensor:
    """Take arbitrary quadrilaterals and reorder their vertices according to their angle
    to the bottommost vertex.

    Args:
        quadrilaterals (Tensor[N, 4, 2]): A batch of quadrilaterals.

    Returns:
        Tensor[N, 4, 2]: The same batch of quadrilaterals, with vertices re-ordered.
    """
    bottommost_idxs = torch.argmin(quadrilaterals[:, :, 1], dim=1)
    bottommost_points = quadrilaterals[
        torch.arange(quadrilaterals.shape[0]), bottommost_idxs
    ].unsqueeze(1)
    shifted = quadrilaterals - bottommost_points
    angles = torch.atan2(shifted[:, :, 1], shifted[:, :, 0])
    angles = torch.where(angles < 0, angles + 2 * torch.pi, angles)  # wrap angles
    # set the angle of the bottommost vertex to -1 to ensure it's first after sorting
    angles[torch.arange(angles.shape[0]), bottommost_idxs] = -1
    _, sorted_indices = torch.sort(angles, dim=1)
    reordered = torch.gather(
        quadrilaterals, 1, sorted_indices.unsqueeze(-1).expand(-1, -1, 2)
    )
    return reordered


def convexify(quadrilaterals: Tensor) -> Tensor:
    """Take arbitrary quadrilaterals and convexify them.

    Args:
        quadrilaterals (Tensor[N, 4, 2]): A batch of quadrilaterals.

    Returns:
        Tensor[N, 4, 2]: The same batch of quadrilaterals, with vertices re-ordered
        and adjusted for concave quadrilaterals.
    """
    uncrossed = uncross(quadrilaterals)
    edges = torch.roll(uncrossed, -1, dims=1) - uncrossed
    cross_products = (
        edges[:, :, 0] * torch.roll(edges, -1, dims=1)[:, :, 1]
        - edges[:, :, 1] * torch.roll(edges, -1, dims=1)[:, :, 0]
    )
    is_concave = torch.any(cross_products < 0, dim=1)
    # For concave quadrilaterals, replace the point opposite to the pivot
    # with the center of the segment bounded by the two other points
    # opposite_point = uncrossed[is_concave, 2]
    center_point = (uncrossed[is_concave, 1] + uncrossed[is_concave, 3]) / 2
    uncrossed[is_concave, 2] = center_point
    return uncrossed
