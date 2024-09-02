from typing import List, Tuple, Dict

from torch import nn, Tensor
from torch.nn.functional import binary_cross_entropy_with_logits, cross_entropy
from torchmetrics import MeanMetric
from torchmetrics.text import WordErrorRate
import torch

from sihl.layers import SequentialConvBlocks


class SceneTextRecognition(nn.Module):
    """Scene text recognition is predicting a sequence of tokens. Tokens can represent
    textual characters, but not necessarily. The prediction is performed in parallel,
    which is fast, but can struggle to predict very long sequences.
    """

    def __init__(
        self,
        in_channels: List[int],
        num_tokens: int,
        max_sequence_length: int,
        level: int = 3,
        num_channels: int = 256,
        num_layers: int = 3,
    ) -> None:
        """
        Args:
            in_channels (List[int]): Number of channels in input feature maps, sorted by level.
            num_tokens (int): Number of possible tokens.
            max_sequence_length (int): Maximum length of predicted sequences.
            level (int, optional): Level of inputs this head is attached to. Defaults to 3.
            num_channels (int, optional): Number of convolutional channels. Defaults to 256.
            num_layers (int, optional): Number of convolutional layers. Defaults to 4.
        """
        assert num_tokens > 0
        assert max_sequence_length > 0
        assert level < len(in_channels)
        super().__init__()

        self.in_channels = in_channels
        self.num_tokens = num_tokens
        self.max_sequence_length = max_sequence_length
        self.level = level

        self.class_head = nn.Sequential(
            SequentialConvBlocks(in_channels[level], num_channels, num_layers),
            nn.Conv2d(num_channels, num_tokens, 1),
        )
        self.index_head = nn.Sequential(
            SequentialConvBlocks(in_channels[level], num_channels, num_layers),
            nn.Conv2d(num_channels, max_sequence_length, 1),
            nn.Sigmoid(),
        )
        self.threshold = 0.5

        self.output_shapes = {
            "scores": ("batch_size", max_sequence_length),
            "tokens": ("batch_size", max_sequence_length),
        }

    def get_maps(self, inputs: List[Tensor]) -> Tuple[Tensor, Tensor]:
        x = inputs[self.level]
        index_map = self.index_head(x)  # (N, L, H, W)
        class_map = self.class_head(x).softmax(dim=1)  # (N, C, H, W)
        return index_map, class_map

    def forward(self, inputs: List[Tensor]) -> Tuple[Tensor, Tensor]:
        x = inputs[self.level]
        index_map = self.index_head(x).flatten(2, 3).unsqueeze(1)  # (N, 1, L, H*W)
        class_map = self.class_head(x).flatten(2, 3).unsqueeze(2)  # (N, C, 1, H*W)
        scores = (class_map * index_map).mean(dim=3).softmax(dim=1)
        return scores.max(dim=1)  # (N, L), (N, L)

    def training_step(
        self, inputs: List[Tensor], tokens: List[Tensor]
    ) -> Tuple[Tensor, Dict[str, float]]:
        x = inputs[self.level]
        index_map = self.index_head(x).flatten(2, 3).unsqueeze(1)  # (N, 1, L, H*W)
        class_map = self.class_head(x).flatten(2, 3).unsqueeze(2)  # (N, C, 1, H*W)
        logits = (class_map * index_map).mean(dim=3)  # (N, C, L)
        with torch.no_grad():
            target = torch.zeros_like(logits)
            for batch_idx, sample_tokens in enumerate(tokens):
                for char_pos, token_idx in enumerate(sample_tokens):
                    target[batch_idx, token_idx, char_pos] = 1
        pos_loss = cross_entropy(logits, target, reduction="mean", label_smoothing=0.1)

        # supervision of "negative" indices and tokens (i.e. those missing in targets)
        neg_index_losses = []
        neg_class_losses = []
        for batch_idx, sample_tokens in enumerate(tokens):
            num_tokens = sample_tokens.shape[0]
            neg_index_map = index_map[batch_idx, 0, num_tokens:, :]
            neg_index_losses.append(
                binary_cross_entropy_with_logits(
                    neg_index_map, torch.zeros_like(neg_index_map), reduction="mean"
                )
            )
            all_indices = torch.arange(0, self.num_tokens, device=pos_loss.device)
            neg_mask = torch.isin(
                all_indices, sample_tokens.unique(), assume_unique=True, invert=True
            )
            neg_class_map = class_map[batch_idx, all_indices[neg_mask], 0, :]
            neg_class_losses.append(
                binary_cross_entropy_with_logits(
                    neg_class_map, torch.zeros_like(neg_class_map), reduction="mean"
                )
            )
        neg_index_loss = torch.stack(neg_index_losses).mean()
        neg_class_loss = torch.stack(neg_class_losses).mean()
        neg_loss = neg_index_loss + neg_class_loss

        return pos_loss + neg_loss, {
            "positive_loss": pos_loss.item(),
            "negative_loss": neg_loss.item(),
        }

    def on_validation_start(self) -> None:
        self.token_error_rate = WordErrorRate()  # space-separated tokens as "words"
        self.loss_computer = MeanMetric(nan_strategy="ignore")
        self.matches: List[bool] = []

    def validation_step(
        self, inputs: List[Tensor], tokens: List[Tensor]
    ) -> Tuple[Tensor, Dict[str, float]]:
        scores, pred_tokens = self.forward(inputs)
        predictions = [
            " ".join(
                str(token.item())
                for score, token in zip(sample_scores, sample_tokens)
                if score > self.threshold
            ).strip()
            for sample_scores, sample_tokens in zip(scores, pred_tokens)
        ]
        ground_truths = [
            " ".join(str(token_idx.item()) for token_idx in label).strip()
            for label in tokens
        ]
        self.token_error_rate.update(predictions, ground_truths)
        self.matches.extend(
            [pred == gt for pred, gt in zip(predictions, ground_truths)]
        )
        loss, metrics = self.training_step(inputs, tokens)
        self.loss_computer.to(loss.device).update(loss)
        return loss, metrics

    def on_validation_end(self) -> Dict[str, float]:
        return {
            "loss": self.loss_computer.compute().item(),
            "token_error_rate": self.token_error_rate.compute().item(),
            "accuracy": sum(self.matches) / len(self.matches),
        }
