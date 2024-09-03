import torch
from torch import nn
from torch.nn import functional as F

class SpatialAttention(nn.Module):
    def __init__(self, in_channels: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conv = nn.Conv2d(in_channels, 1, kernel_size=1, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        attention = F.sigmoid(self.conv(x))
        return x * attention