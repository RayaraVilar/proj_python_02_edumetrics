from pathlib import Path

import pandas as pd
import torch
from torch import nn

from .models import DropoutRiskModel


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "datasets" / "training_students.csv"
MODEL_DIR = BASE_DIR / "predictions" / "artifacts"
MODEL_PATH = MODEL_DIR / "dropout_model.pth"


def prepare_dataset():
    dataframe = pd.read_csv(DATASET_PATH)

    feature_columns = [
        "attendance_rate",
        "average_grade",
        "platform_accesses",
        "activity_completion",
        "study_hours_per_week",
    ]

    features = dataframe[feature_columns].copy()
    targets = dataframe["dropped_out"].copy()

    features["attendance_rate"] /= 100
    features["average_grade"] /= 10
    features["platform_accesses"] /= 100
    features["study_hours_per_week"] /= 20

    features_tensor = torch.tensor(
        features.values,
        dtype=torch.float32,
    )

    targets_tensor = torch.tensor(
        targets.values,
        dtype=torch.float32,
    ).reshape(-1, 1)

    return features_tensor, targets_tensor


def train_model(epochs=1500, learning_rate=0.01):
    torch.manual_seed(42)

    features, targets = prepare_dataset()

    model = DropoutRiskModel()

    loss_function = nn.BCELoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate,
    )

    model.train()

    for epoch in range(epochs):
        predictions = model(features)

        loss = loss_function(predictions, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 100 == 0:
            print(
                f"Epoch {epoch + 1}/{epochs} "
                f"- Loss: {loss.item():.6f}"
            )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    torch.save(
        model.state_dict(),
        MODEL_PATH,
    )

    print(f"\nModelo salvo em: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()