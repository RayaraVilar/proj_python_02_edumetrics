from django.db import models

# Create your models here.
import torch
from torch import nn


class DropoutRiskModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(5, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid(),
        )

    def forward(self, features):
        return self.network(features)