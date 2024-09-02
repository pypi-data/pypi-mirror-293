from functools import partial
from typing import List, Tuple, Dict, Optional

from torch import nn, Tensor
from torchmetrics import MeanAbsoluteError, MeanSquaredError, MeanMetric

from sihl.layers import ConvNormAct, BilinearAdditiveUpscaler, SequentialConvBlocks
from sihl.utils import interpolate


sequential_upscalers = partial(SequentialConvBlocks, ConvBlock=BilinearAdditiveUpscaler)


class Autoencoding(nn.Module):
    """Autoencoding is reconstructing an image by encoding it into a compact
    representation and then decoding that into the initial input. The point of learning
    this is that the representation can be used for downstream tasks like clustering.
    This task is self-supervised, so it can be a good choice for pre-training backbones.

    Todo:
        - [Diffusion Autoencoders](https://arxiv.org/abs/2111.15640)
    """

    def __init__(
        self,
        in_channels: List[int],
        level: int = 5,
        num_channels: int = 256,
        num_layers: int = 1,
        representation_channels: int = 128,
        activation: Optional[str] = "sigmoid",
    ):
        """
        Args:
            in_channels (List[int]): Number of channels in input feature maps, sorted by level.
            level (int, optional): Level of inputs this head is attached to. Defaults to 5.
            num_channels (int, optional): Number of convolutional channels. Defaults to 256.
            num_layers (int, optional): Number of convolutional layers. Defaults to 1.
            representation_channels (int, optional): Number of channels in the compact representation. Defaults to 128.
            activation (Optional[str], optional): Activation function of the last layer. Defaults to "sigmoid".
        """
        assert num_channels > 0 and num_layers > 0
        assert len(in_channels) > level > 0
        super().__init__()

        self.level = level
        self.encoder = SequentialConvBlocks(
            in_channels[level], representation_channels, num_layers
        )
        self.decoder = nn.Sequential(
            ConvNormAct(representation_channels, num_channels, kernel_size=1),
            sequential_upscalers(num_channels, num_channels, num_layers=level),
            ConvNormAct(num_channels, in_channels[0], act=activation),
        )

        self.output_shapes = {
            "reconstructions": ("batch_size", in_channels[0], "height", "width"),
            "representations": (
                "batch_size",
                representation_channels,
                f"height/{2**level}",
                f"width/{2**level}",
            ),
        }

    def encode(self, inputs: List[Tensor]) -> Tensor:
        return self.encoder(inputs[self.level])

    def encode_decode(self, inputs: List[Tensor]) -> Tensor:
        size = inputs[0].shape[2:]
        embeddings = self.encode(inputs)
        return interpolate(self.decoder(embeddings), size=size).contiguous(), embeddings

    def forward(self, inputs: List[Tensor]) -> Tensor:
        return self.encode_decode(inputs)

    def training_step(
        self, inputs: List[Tensor], targets: Tensor
    ) -> Tuple[Tensor, Dict[str, float]]:
        reconstructions, _ = self.encode_decode(inputs)
        loss = (reconstructions - targets).cosh().log().mean()
        return loss, {}

    def on_validation_start(self) -> None:
        self.loss_computer = MeanMetric(nan_strategy="ignore")
        self.mae_computer = MeanAbsoluteError()
        self.mse_computer = MeanSquaredError()

    def validation_step(
        self, inputs: List[Tensor], targets: Tensor
    ) -> Tuple[Tensor, Dict[str, float]]:
        reconstructions, embeddings = self.encode_decode(inputs)
        loss = (reconstructions - targets).cosh().log().mean()
        self.loss_computer.to(loss.device).update(loss)
        self.mae_computer.to(loss.device).update(reconstructions, targets)
        self.mse_computer.to(loss.device).update(reconstructions, targets)
        return loss, {}

    def on_validation_end(self) -> Dict[str, float]:
        return {
            "loss": self.loss_computer.compute().item(),
            "mean_absolute_error": self.mae_computer.compute().item(),
            "mean_squared_error": self.mse_computer.compute().item(),
        }
