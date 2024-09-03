import torch
from torch import nn
from torch.nn import functional as F

class ChannelAttention(nn.Module):
    def __init__(self, in_channels: int, reduction_ratio=16):
        """Channel attention implementation."""
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        
        self.fc = nn.Sequential(
            nn.Linear(in_channels, in_channels // reduction_ratio, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(in_channels // reduction_ratio, in_channels, bias=False)
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg_out = self.fc(self.avg_pool(x).view(x.size(0), x.size(1)))
        max_out = self.fc(self.max_pool(x).view(x.size(0), x.size(1)))
        return x * F.sigmoid(avg_out + max_out).expand_as(x)