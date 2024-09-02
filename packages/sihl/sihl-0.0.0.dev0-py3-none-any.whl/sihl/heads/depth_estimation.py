from typing import List, Tuple, Dict

from torch import nn, Tensor
from torch.nn import functional
from torchmetrics import MeanMetric
from torchmetrics.regression import MeanAbsoluteError, MeanSquaredError
import torch

from sihl.heads.semantic_segmentation import SemanticSegmentation
from sihl.layers import SequentialConvBlocks
from sihl.utils import interpolate, EPS


class DepthEstimation(SemanticSegmentation):
    """Depth estimation is pixelwise regression.

    Refs:
        1. [Adabins](https://arxiv.org/abs/2011.14141)
    """

    def __init__(
        self,
        in_channels: List[int],
        lower_bound: float,
        upper_bound: float,
        bottom_level: int = 3,
        top_level: int = 5,
        num_channels: int = 256,
        num_layers: int = 1,
        num_bins: int = 256,
    ) -> None:
        """
        Args:
            in_channels (List[int]): Number of channels in input feature maps, sorted by level.
            lower_bound (float): Lower bound of the interval of possible values.
            upper_bound (float): Upper bound of the interval of possible values.
            bottom_level (int, optional): Bottom level of inputs this head is attached to. Defaults to 3.
            top_level (int, optional): Top level of inputs this head is attached to. Defaults to 7.
            num_channels (int, optional): Number of convolutional channels. Defaults to 256.
            num_layers (int, optional): Number of convolutional layers. Defaults to 4.
            num_bins (int, optional): Number of dynamic-sized bins. Defaults to 256.
        """
        assert lower_bound < upper_bound
        assert len(in_channels) > top_level >= bottom_level > 0
        assert num_channels > 0 and num_layers > 0
        assert num_bins > 1
        super().__init__(
            in_channels=in_channels,
            num_classes=num_bins,
            num_channels=num_channels,
            bottom_level=bottom_level,
            top_level=top_level,
            num_layers=num_layers,
            ignore_index=0,
        )

        self.num_bins = num_bins
        self.lower_bound, self.upper_bound = lower_bound, upper_bound
        self.bin_head = nn.Sequential(
            SequentialConvBlocks(in_channels[top_level], num_channels, num_layers),
            nn.Conv2d(num_channels, num_bins, kernel_size=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
        )

        self.output_shapes = {
            "depth_maps": (
                "batch_size",
                f"height/{2**bottom_level}",
                f"width/{2**bottom_level}",
            )
        }

    def normalize(self, x: Tensor) -> Tensor:
        return (x - self.lower_bound) / (self.upper_bound - self.lower_bound)

    def denormalize(self, x: Tensor) -> Tensor:
        return x * (self.upper_bound - self.lower_bound) + self.lower_bound

    def get_bin_centers(self, inputs: List[Tensor]) -> Tensor:
        bin_widths = self.bin_head(inputs[self.top_level]) + EPS
        bin_widths = bin_widths / bin_widths.sum(dim=1, keepdim=True)
        return bin_widths.cumsum(dim=1) - bin_widths / 2

    def get_depth_map(self, inputs: List[Tensor], bin_centers: Tensor) -> Tensor:
        weights = self.get_logits(inputs).relu() + EPS
        weights = weights / weights.sum(dim=1, keepdim=True)
        depth_map = (bin_centers[:, :, None, None] * weights).sum(1, keepdim=True)
        return depth_map.clamp(0, 1)

    def forward(self, inputs: List[Tensor]) -> Tensor:
        bin_centers = self.get_bin_centers(inputs)
        depth_map = self.denormalize(self.get_depth_map(inputs, bin_centers))
        return interpolate(depth_map, size=inputs[0].shape[-2:]).squeeze(1)

    def training_step(
        self, inputs: List[Tensor], targets: Tensor, masks: Tensor
    ) -> Tuple[Tensor, Dict[str, float]]:
        bin_centers = self.get_bin_centers(inputs)
        depth_map = self.get_depth_map(inputs, bin_centers=bin_centers)

        batch_size, target_height, target_width = targets.shape
        pred_height, pred_width = depth_map.shape[2:]
        targets = self.normalize(targets)

        depth_map = interpolate(depth_map, size=(target_height, target_width))
        g = (depth_map.squeeze(1)[masks] + EPS).log() - (targets[masks] + EPS).log()
        pixel_loss = torch.sqrt(g.var() + 0.15 * g.mean() ** 2) * 10

        hist_losses = []
        for batch_idx in range(batch_size):
            target_hist = targets[batch_idx].reshape(1, 1, target_height, target_width)
            target_hist = interpolate(target_hist, size=(pred_height, pred_width))
            hist_mask = masks[batch_idx].reshape(1, 1, target_height, target_width)
            hist_mask = functional.interpolate(
                hist_mask.to(torch.float),
                size=(pred_height, pred_width),
                mode="nearest-exact",
            )
            target_hist = target_hist[hist_mask > 0.5].reshape(1, -1, 1, 1)
            pred_hist = bin_centers[batch_idx].reshape(1, 1, -1, 1)
            # bidirectional chamfer loss
            dist = ((pred_hist - target_hist) ** 2).sum(dim=-1)
            forward_chamfer = torch.min(dist, dim=2)[0].mean(dim=1)
            backward_chamfer = torch.min(dist, dim=1)[0].mean(dim=1)
            hist_losses.append((forward_chamfer + backward_chamfer).mean())
        hist_loss = torch.stack(hist_losses).mean()

        return pixel_loss + hist_loss, {
            "pixel_loss": pixel_loss,
            "hist_loss": hist_loss,
        }

    def on_validation_start(self) -> None:
        self.loss_computer = MeanMetric(nan_strategy="ignore")
        self.mae_computer = MeanAbsoluteError()
        self.rmse_computer = MeanSquaredError(squared=False)

    def validation_step(
        self, inputs: List[Tensor], targets: Tensor, masks: Tensor
    ) -> Tuple[Tensor, Dict[str, float]]:
        loss, _ = self.training_step(inputs, targets, masks)
        device = loss.device
        self.loss_computer.to(device).update(loss)
        depth_map = self.forward(inputs)
        batch_size, pred_height, pred_width = depth_map.shape
        self.rmse_computer.to(device).update(depth_map[masks], targets[masks])
        self.mae_computer.to(device).update(depth_map[masks], targets[masks])
        return loss, {}

    def on_validation_end(self) -> Dict[str, float]:
        return {
            "loss": self.loss_computer.compute().item(),
            "rmse": self.rmse_computer.compute().item(),
            "mae": self.mae_computer.compute().item(),
        }
