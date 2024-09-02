from functools import partial
from typing import List, Dict, Tuple, Optional

from torch import nn, Tensor
from torchmetrics import MeanMetric, JaccardIndex, Accuracy
import torch

from sihl.layers import (
    StridedDownscaler,
    SimpleUpscaler,
    ConvNormAct,
    Normalize,
    SequentialConvBlocks,
)
from sihl.utils import interpolate

sequential_downscalers = partial(SequentialConvBlocks, ConvBlock=StridedDownscaler)
sequential_upscalers = partial(SequentialConvBlocks, ConvBlock=SimpleUpscaler)


class AnomalyDetection(nn.Module):
    """Anomaly detection is telling whether an image contains an "anomaly" or not. The
    difference with binary classification is that this head only needs "positive samples"
    (i.e. "normal" images) to train on, whereas the binary classification head would
    need those and a similar amount of "negative samples" (i.e. "anomalous" images).
    This task is self-supervised, but it needs labeled samples (positive and negative)
    for validation.

    As described in [1], this head has 3 "submodels":
    1. a pre-trained frozen teacher, which extracts generic image features
    2. an autoencoder, which extracts compact features by attempting to recreate the
       input through a bottleneck
    3. a student model, which tries to match the outputs of the previous 2 submodels

    At prediction time, the difference between the student and the teacher highlights
    structural (local) anomalies, while the difference between the student and the
    autoencoder shows logical (global) anomalies.

    Refs:
        1. [EfficientAD](https://arxiv.org/abs/2303.14535)
    """

    def __init__(
        self,
        in_channels: List[int],
        bottom_level: int = 2,
        top_level: int = 3,
        num_channels: int = 256,
        num_layers: int = 3,
        autoencoder_channels: int = 64,
        autoencoder_top_level: int = 5,
    ):
        """
        Args:
            in_channels (List[int]): Number of channels in input feature maps, sorted by level.
            bottom_level (int, optional): Bottom level of inputs this head is attached to. Defaults to 2.
            top_level (int, optional): Top level of inputs this head is attached to. Defaults to 3.
            num_channels (int, optional): Number of convolutional channels. Defaults to 256.
            num_layers (int, optional): Number of convolutional layers. Defaults to 3.
            autoencoder_channels (int, optional): Number of channels in the compact representation. Defaults to 64.
            autoencoder_top_level (int, optional): Top level of inputs the autoencoder is attached to. Defaults to 5.
        """
        assert num_channels > 0 and num_layers > 0
        assert len(in_channels) > top_level >= bottom_level > 0
        super().__init__()

        self.bottom_level = bottom_level
        self.top_level = top_level
        self.levels = range(bottom_level, top_level + 1)
        self.num_channels = num_channels
        self.num_layers = num_layers
        self.q_hard = 0.999
        self.autoencoder_top_level = autoencoder_top_level

        self.out_channels = sum([in_channels[_] for _ in self.levels])
        self.normalize = Normalize(mean=[0.5], std=[0.5])
        self.student = nn.Sequential(
            ConvNormAct(in_channels[0], num_channels),
            sequential_downscalers(num_channels, num_channels, num_layers=bottom_level),
            SequentialConvBlocks(num_channels, num_channels, num_layers=num_layers),
            nn.Conv2d(num_channels, self.out_channels * 2, kernel_size=1),
        )
        self.autoencoder = nn.Sequential(
            ConvNormAct(in_channels[0], num_channels),
            sequential_downscalers(
                num_channels, num_channels, num_layers=autoencoder_top_level
            ),
            ConvNormAct(num_channels, autoencoder_channels),
            sequential_upscalers(
                autoencoder_channels, num_channels, autoencoder_top_level - bottom_level
            ),
            nn.Conv2d(num_channels, self.out_channels, kernel_size=1),
        )
        self.register_buffer("q_st_start", torch.tensor(0))
        self.register_buffer("q_st_end", torch.tensor(0.1))
        self.register_buffer("q_ae_start", torch.tensor(0))
        self.register_buffer("q_ae_end", torch.tensor(0.1))

        self.output_shapes = {
            "anomaly_maps": (
                "batch_size",
                f"height/{2**bottom_level}",
                f"width/{2**bottom_level}",
            )
        }

    def teacher_project(self, inputs: List[Tensor]) -> Tensor:
        size = inputs[self.bottom_level].shape[2:]
        features = torch.cat(
            [interpolate(inputs[level], size=size) for level in self.levels], dim=1
        )
        features = (features - features.mean()) / features.std()
        return features

    def compute_distances(self, inputs: List[Tensor]) -> Tensor:
        image = self.normalize(inputs[0])
        teacher_out = self.teacher_project(inputs)
        student_out = self.student(image)
        autoencoder_out = self.autoencoder(image)
        st_teacher = student_out[:, : self.out_channels]
        st_teacher = (st_teacher - st_teacher.mean()) / st_teacher.std()  ## ?
        st_autoencoder = student_out[:, self.out_channels :]
        distance_st = (teacher_out - st_teacher) ** 2
        distance_ae = (autoencoder_out - teacher_out) ** 2
        distance_stae = (autoencoder_out - st_autoencoder) ** 2
        return distance_st, distance_ae, distance_stae

    def forward(self, inputs: List[Tensor]) -> Tensor:
        distance_st, distance_ae, distance_stae = self.compute_distances(inputs)
        anomaly_local = distance_st.mean(dim=1, keepdim=True)
        anomaly_global = distance_stae.mean(dim=1, keepdim=True)
        anomaly_local = (
            0.1 * (anomaly_local - self.q_st_start) / (self.q_st_end - self.q_st_start)
        )
        anomaly_global = (
            0.1 * (anomaly_global - self.q_ae_start) / (self.q_ae_end - self.q_ae_start)
        )
        anomaly = (0.5 * (anomaly_local + anomaly_global)).clamp(0, 1)
        return interpolate(anomaly, size=inputs[0].shape[2:]).squeeze(1)

    def training_step(
        self, inputs: List[Tensor], targets: Optional[Tensor] = None
    ) -> Tuple[Tensor, Dict[str, float]]:
        # TODO: augment autoencoder input
        distance_st, distance_ae, distance_stae = self.compute_distances(inputs)
        st_losses = []
        for x in distance_st:  # https://github.com/pytorch/pytorch/issues/64947
            d_hard = torch.quantile(x, q=self.q_hard)
            st_losses.append(x[x >= d_hard].mean())
        loss_st = torch.stack(st_losses).mean()
        loss_ae = distance_ae.mean()
        loss_stae = distance_stae.mean()
        return loss_st + loss_ae + loss_stae, {
            "loss_student_teacher": loss_st,
            "loss_autoencoder_teacher": loss_ae,
            "loss_student_autoencoder": loss_stae,
        }

    def on_validation_start(self) -> None:
        self.loss_computer = MeanMetric(nan_strategy="ignore")
        self.mean_iou_computer = JaccardIndex(task="binary")
        self.accuracy = Accuracy(task="binary")
        self.maps_st, self.maps_ae = [], []

    def validation_step(
        self, inputs: List[Tensor], targets: Optional[Tensor] = None
    ) -> Tuple[Tensor, Dict[str, float]]:
        distance_st, distance_ae, distance_stae = self.compute_distances(inputs)
        self.maps_st.append(distance_st.mean(dim=1))
        self.maps_ae.append(distance_stae.mean(dim=1))
        loss, metrics = self.training_step(inputs)
        if targets is not None:
            pred = self.forward(inputs)
            self.mean_iou_computer.to(loss.device).update(pred, targets)
            self.accuracy.to(loss.device).update(
                (pred > 0.5).any(dim=(1, 2)), targets.any(dim=(1, 2))
            )
        self.loss_computer.to(loss.device).update(loss)
        return loss, metrics

    def on_validation_end(self) -> Dict[str, float]:
        maps_st, maps_ae = torch.cat(self.maps_st), torch.cat(self.maps_ae)
        del self.maps_st, self.maps_ae
        self.q_st_start = torch.quantile(maps_st, q=0.9)
        self.q_st_end = torch.quantile(maps_st, q=0.95)
        self.q_ae_start = torch.quantile(maps_ae, q=0.9)
        self.q_ae_end = torch.quantile(maps_ae, q=0.95)
        return {
            "loss": self.loss_computer.compute().item(),
            "mean_iou": self.mean_iou_computer.compute().item(),
            "accuracy": self.accuracy.compute().item(),
        }
