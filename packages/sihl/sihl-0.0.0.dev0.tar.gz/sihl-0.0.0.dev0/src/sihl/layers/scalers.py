from functools import partial

from torch import Tensor, nn
from torch.nn import functional

from sihl.layers.convblocks import ConvNormAct
from sihl.layers.pooling import BlurPool2d

interpolate = partial(
    functional.interpolate, mode="bilinear", antialias=False, align_corners=False
)


class StridedDownscaler(ConvNormAct):
    def __init__(self, in_channels: int, out_channels: int, **kwargs) -> None:
        super().__init__(in_channels, out_channels, stride=2, **kwargs)


class AntialiasedDownscaler(nn.Sequential):
    def __init__(
        self, in_channels: int, out_channels: int, kernel_size: int = 3
    ) -> None:
        super().__init__(
            ConvNormAct(in_channels, out_channels, kernel_size),
            BlurPool2d(out_channels, stride=2),
        )


class BilinearScaler(nn.Module):
    def __init__(self, scale: float = 2.0) -> None:
        super().__init__()
        self.scale = scale

    def forward(self, x: Tensor) -> Tensor:
        return interpolate(x, scale_factor=self.scale)


class SimpleUpscaler(nn.Sequential):
    def __init__(
        self, in_channels: int, out_channels: int, kernel_size: int = 3
    ) -> None:
        super().__init__(
            BilinearScaler(2.0), ConvNormAct(in_channels, out_channels, kernel_size)
        )


class BilinearAdditiveUpscaler(nn.Module):
    """[The Devil is in the Decoder](https://arxiv.org/abs/1707.05847)"""

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3):
        super().__init__()
        self.residual = nn.ConvTranspose2d(
            in_channels, in_channels // 4, kernel_size=2, stride=2
        )
        self.out_conv = ConvNormAct(
            in_channels // 4, out_channels, kernel_size=kernel_size
        )

    def forward(self, x: Tensor) -> Tensor:
        residual = self.residual(x)
        x = interpolate(x, scale_factor=2)
        batch_size, num_channels, height, width = x.shape
        x = x.reshape(batch_size, num_channels // 4, 4, height, width).mean(dim=2)
        return self.out_conv(x + residual)
