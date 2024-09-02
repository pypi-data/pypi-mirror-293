from math import log
from typing import List
import logging

from torch import Tensor, nn
import timm
import torch

from sihl.layers import Normalize, PadToMultipleOf

TIMM_BACKBONE_NAMES = (
    "convnext_atto",
    "convnext_base",
    "convnext_femto",
    "convnext_large",
    "convnext_nano",
    "convnext_pico",
    "convnext_small",
    "convnext_tiny",
    "convnext_xlarge",
    "convnext_xxlarge",
    "convnextv2_atto",
    "convnextv2_base",
    "convnextv2_femto",
    "convnextv2_huge",
    "convnextv2_large",
    "convnextv2_nano",
    "convnextv2_pico",
    "convnextv2_small",
    "convnextv2_tiny",
    "dla34",
    "dla60",
    "dla102",
    "dla169",
    "efficientnet_b0",
    "efficientnet_b1",
    "efficientnet_b2",
    "efficientnet_b3",
    "efficientnet_b4",
    "efficientnet_b5",
    "efficientnet_b6",
    "efficientnet_b7",
    "efficientnet_b8",
    "efficientnet_lite0",
    "efficientnet_lite1",
    "efficientnet_lite2",
    "efficientnet_lite3",
    "efficientnet_lite4",
    "efficientnetv2_l",
    "efficientnetv2_m",
    "efficientnetv2_s",
    "efficientnetv2_xl",
    "hrnet_w18",
    "hrnet_w30",
    "hrnet_w32",
    "hrnet_w40",
    "hrnet_w44",
    "hrnet_w48",
    "hrnet_w64",
    "mobilenet_100",
    "mobilenet_125",
    "mobilenetv2_035",
    "mobilenetv2_050",
    "mobilenetv2_075",
    "mobilenetv2_100",
    "mobilenetv2_140",
    "mobilenetv3_large_075",
    "mobilenetv3_large_100",
    "mobilenetv3_small_050",
    "mobilenetv3_small_075",
    "mobilenetv3_small_100",
    "mobilenetv4_conv_large",
    "mobilenetv4_conv_medium",
    "mobilenetv4_conv_small",
    "mobilenetv4_hybrid_large",
    "mobilenetv4_hybrid_large_075",
    "mobilenetv4_hybrid_medium",
    "mobilenetv4_hybrid_medium_075",
    "resnet18",
    "resnet26",
    "resnet34",
    "resnet50",
    "resnet101",
    "resnet152",
    "resnet200",
    "resnetv2_50",
    "resnetv2_101",
    "resnetv2_152",
)


class TimmBackbone(nn.Module):
    """https://github.com/huggingface/pytorch-image-models"""

    def __init__(
        self,
        name: str,
        pretrained: bool = False,
        input_channels: int = 3,
        frozen_levels: int = 0,
    ) -> None:
        super().__init__()
        self.name = name
        self.dummy_input = torch.zeros((4, input_channels, 64, 64))
        try:
            reds = timm.create_model(name, features_only=True).feature_info.reduction()
            assert all(log(reduction, 2).is_integer() for reduction in reds)
            self.model = timm.create_model(
                self.name,
                features_only=True,
                out_indices=(0, 1, 2, 3, 4),
                scriptable=True,
                exportable=True,
                pretrained=pretrained,
                in_chans=input_channels,
            )
            self.model(self.dummy_input)
        except (RuntimeError, AttributeError, AssertionError) as error:
            raise ValueError(f'Architecture "{name}" is not supported.') from error
        self.normalize = (
            Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
            if pretrained and input_channels == 3
            else Normalize(mean=(0.5,), std=(0.5,))
        )
        self.pad = PadToMultipleOf(32)
        # freeze modules in first `frozen_levels` levels
        for parameter in self.model.parameters():
            parameter.requires_grad = True
        if frozen_levels != 0:
            len_levels = len(self.model.feature_info.module_name())
            frozen_levels = (
                len_levels if frozen_levels < 0 else min(frozen_levels, len_levels)
            )
            stop_freeze = self.model.feature_info.module_name()[frozen_levels - 1]
            last_level_reached = False
            for layer_name in [_[0] for _ in self.model.named_modules()]:
                if last_level_reached:
                    break
                if layer_name == "" or "." in layer_name:
                    continue
                if stop_freeze in layer_name:
                    last_level_reached = True
                logging.info(f"freezing {layer_name}")
                for parameter in getattr(self.model, layer_name).parameters():
                    parameter.requires_grad = False
                    if isinstance(parameter, nn.BatchNorm2d):
                        parameter.track_running_stats = False
                        parameter.eval()
        self.out_channels = [input_channels] + self.model.feature_info.channels()

    def forward(self, x: Tensor) -> List[Tensor]:
        return [x] + list(self.model(self.pad(self.normalize(x))))
