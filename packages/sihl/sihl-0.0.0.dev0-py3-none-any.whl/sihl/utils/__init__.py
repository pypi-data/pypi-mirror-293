# ruff: noqa: F401
from typing import Any, Tuple, List, Callable, Union
import functools
import random
import sys

from torch import Tensor
from torch.nn import functional
import torch
import torchvision

from sihl.utils.polygon_iou import polygon_iou


EPS = 1e-5
interpolate = functools.partial(
    functional.interpolate, mode="bilinear", antialias=False, align_corners=False
)


def random_pad(
    image: Tensor, target_size: Union[int, Tuple[int, int]], fill: Union[float, int] = 0
) -> Tensor:
    image_size = image.shape[1:]
    if isinstance(target_size, int):
        target_size = (target_size, target_size)

    if image_size[0] > target_size[0] or image_size[1] > target_size[1]:
        scale_factor = min(
            target_size[0] / image_size[0], target_size[1] / image_size[1]
        )
        new_height = int(image_size[0] * scale_factor)
        new_width = int(image_size[1] * scale_factor)
        image = torchvision.transforms.functional.resize(image, (new_height, new_width))
        image_size = image.shape[1:]

    pad_width = target_size[1] - image_size[1]
    pad_height = target_size[0] - image_size[0]

    top_pad = random.randint(0, pad_height)
    bottom_pad = pad_height - top_pad
    left_pad = random.randint(0, pad_width)
    right_pad = pad_width - left_pad

    padded_image = torchvision.transforms.functional.pad(
        image, (left_pad, top_pad, right_pad, bottom_pad), fill
    )
    return padded_image


def coordinate_grid(height: int, width: int, y_max: float, x_max: float) -> Tensor:
    """2D grid of pixel center coordinates (0 to x_max, 0 to y_max)."""
    y_max, x_max = torch.scalar_tensor(y_max), torch.scalar_tensor(x_max)
    y_min, x_min = y_max / height / 2, x_max / width / 2
    ys = torch.linspace(y_min, y_max - y_min, steps=height)
    xs = torch.linspace(x_min, x_max - x_min, steps=width)
    return torch.stack([xs[None, :].repeat(height, 1), ys[:, None].repeat(1, width)])


def f_beta(beta: float) -> Callable[[Tensor, Tensor], Tensor]:
    """https://en.wikipedia.org/wiki/F-score#Definition"""
    return lambda p, r: (1 + beta**2) * p * r / (beta**2 * p + r)


def points_to_bbox(points: Tensor) -> Tensor:
    """(N, K, 2) -> (N, 4)"""
    min_x = torch.min(points[..., 0], dim=1).values
    min_y = torch.min(points[..., 1], dim=1).values
    max_x = torch.max(points[..., 0], dim=1).values
    max_y = torch.max(points[..., 1], dim=1).values
    return torch.stack([min_x, min_y, max_x, max_y], dim=1)


def inverse_sigmoid(x: Tensor) -> Tensor:
    x = x.clamp(min=EPS, max=1 - EPS)
    return torch.log(x / (1 - x))


def edges(x: Tensor) -> Tensor:
    sobel_kernel_x = torch.tensor(
        [[[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]]], dtype=x.dtype, device=x.device
    )
    sobel_kernel_y = torch.tensor(
        [[[[-1, -2, -1], [0, 0, 0], [1, 2, 1]]]], dtype=x.dtype, device=x.device
    )
    sobel_kernel_x = sobel_kernel_x.repeat(x.shape[1], 1, 1, 1)
    sobel_kernel_y = sobel_kernel_y.repeat(x.shape[1], 1, 1, 1)
    edges_x = functional.conv2d(x, sobel_kernel_x, padding=1, groups=x.shape[1])
    edges_y = functional.conv2d(x, sobel_kernel_y, padding=1, groups=x.shape[1])
    edges = torch.sqrt(edges_x**2 + edges_y**2)
    edges = edges / edges.max()
    return edges


def recursive_getattr(obj: Any, attr: str, *args):
    """https://stackoverflow.com/a/31174427"""

    def _getattr(obj: Any, attr: str):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


def recursive_setattr(obj: Any, attr: str, val: Any):
    """https://stackoverflow.com/a/31174427"""
    pre, _, post = attr.rpartition(".")
    return setattr(recursive_getattr(obj, pre) if pre else obj, post, val)


def call_and_get_locals(func: Callable, *args, **kwargs) -> Tuple[Any, List[Any]]:
    """https://stackoverflow.com/a/52358426"""
    frame = None

    def snatch_locals(_frame, name, arg):
        nonlocal frame
        if name == "call":
            frame = _frame
            sys.settrace(sys._getframe(0).f_trace)
        return sys._getframe(0).f_trace

    sys.settrace(snatch_locals)

    try:
        result = func(*args, **kwargs)
    finally:
        sys.settrace(sys._getframe(0).f_trace)

    return result, frame.f_locals
