from typing import Tuple, List, Union, Dict

from torch import nn, Tensor
from torch.nn.functional import cross_entropy
from torchmetrics import JaccardIndex, MeanMetric, Accuracy
import torch

from sihl.layers import ConvNormAct, SequentialConvBlocks
from sihl.utils import interpolate, EPS


class SemanticSegmentation(nn.Module):
    """Semantic segmentation is pixelwise multiclass classification.

    Refs:
        1. [ESeg](https://arxiv.org/abs/2203.12683)
    """

    def __init__(
        self,
        in_channels: List[int],
        num_classes: int,
        bottom_level: int = 3,
        top_level: int = 5,
        num_channels: int = 256,
        num_layers: int = 1,
        ignore_index: Union[int, None] = None,
    ) -> None:
        """
        Args:
            in_channels (List[int]): Number of channels in input feature maps, sorted by level.
            num_classes (int): Number of possible pixel categories.
            bottom_level (int, optional): Bottom level of inputs this head is attached to. Defaults to 3.
            top_level (int, optional): Top level of inputs this head is attached to. Defaults to 7.
            num_channels (int, optional): Number of convolutional channels. Defaults to 256.
            num_layers (int, optional): Number of convolutional layers. Defaults to 4.
            ignore_index (Union[int, None], optional): Ignored category index. Defaults to None.
        """
        assert num_classes > 0
        assert len(in_channels) > top_level >= bottom_level > 0
        assert num_channels > 0 and num_layers > 0
        super().__init__()

        self.in_channels = in_channels
        self.num_classes = num_classes
        self.num_channels = num_channels
        self.num_layers = num_layers
        self.bottom_level = bottom_level
        self.top_level = top_level
        self.ignore_index = ignore_index or -100
        self.sum_weights = nn.Parameter(torch.ones(top_level - bottom_level + 1))

        # input channels need to be matched if they aren't already
        matched_channels = in_channels[bottom_level]
        self.lateral_convs = None
        level_channels = in_channels[bottom_level : top_level + 1]
        if not all(_ == matched_channels for _ in level_channels):
            matched_channels = num_channels
            self.lateral_convs = [
                ConvNormAct(_, num_channels, kernel_size=1) for _ in level_channels
            ]

        self.out_conv = nn.Sequential(
            SequentialConvBlocks(matched_channels, num_channels, num_layers),
            nn.Conv2d(num_channels, num_classes, kernel_size=1),
        )

        self.output_shapes = {
            "score_maps": ("batch_size", "height", "width"),
            "class_maps": ("batch_size", "height", "width"),
        }

    def get_logits(self, inputs: List[Tensor]) -> Tensor:
        inputs = inputs[self.bottom_level : self.top_level + 1]
        if self.lateral_convs:
            inputs = [conv(x) for x, conv in zip(inputs, self.lateral_convs)]
        weights = self.sum_weights.relu() + EPS
        weights = weights / weights.max()
        size = inputs[0].shape[2:]
        return self.out_conv(
            sum(w * interpolate(x, size=size) for w, x in zip(weights, inputs))
        )

    def forward(self, inputs: List[Tensor]) -> Tuple[Tensor, Tensor]:
        x = interpolate(self.get_logits(inputs), size=inputs[0].shape[2:])
        return x.softmax(dim=1).max(dim=1)

    def training_step(
        self, inputs: List[Tensor], targets: Tensor
    ) -> Tuple[Tensor, Dict[str, float]]:
        logits = interpolate(self.get_logits(inputs), size=targets.shape[1:])
        loss = cross_entropy(logits, targets, ignore_index=self.ignore_index)
        return loss, {}

    def on_validation_start(self) -> None:
        self.loss_computer = MeanMetric(nan_strategy="ignore")
        metric_kwargs = {
            "task": "multiclass",
            "num_classes": self.num_classes,
            "ignore_index": self.ignore_index,
        }
        self.pixel_accuracy = Accuracy(**metric_kwargs)
        self.mean_iou_computer = JaccardIndex(**metric_kwargs)

    def validation_step(
        self, inputs: List[Tensor], targets: Tensor
    ) -> Tuple[Tensor, Dict[str, float]]:
        logits = interpolate(self.get_logits(inputs), size=targets.shape[1:])
        loss = cross_entropy(logits, targets, ignore_index=self.ignore_index)
        scores = logits.softmax(dim=1)
        self.mean_iou_computer.to(loss.device).update(scores, targets)
        self.pixel_accuracy.to(loss.device).update(scores, targets)
        self.loss_computer.to(loss.device).update(loss)
        return loss, {}

    def on_validation_end(self) -> Dict[str, float]:
        return {
            "loss": self.loss_computer.compute().item(),
            "pixel_accuracy": self.pixel_accuracy.compute().item(),
            "mean_iou": self.mean_iou_computer.compute().item(),
        }
