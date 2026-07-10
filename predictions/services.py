from functools import lru_cache
from pathlib import Path

import torch

from .models import DropoutRiskModel


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "predictions"
    / "artifacts"
    / "dropout_model.pth"
)


class DropoutPredictor:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Modelo não encontrado. Execute: "
                "python -m predictions.train_model"
            )

        self.model = DropoutRiskModel()

        state_dict = torch.load(
            MODEL_PATH,
            map_location="cpu",
            weights_only=True,
        )

        self.model.load_state_dict(state_dict)
        self.model.eval()

    def predict(
        self,
        attendance_rate,
        average_grade,
        platform_accesses,
        completed_activities,
        total_activities,
        study_hours_per_week,
    ):
        if total_activities > 0:
            activity_completion = (
                completed_activities / total_activities
            )
        else:
            activity_completion = 0

        features = torch.tensor(
            [
                [
                    attendance_rate / 100,
                    average_grade / 10,
                    platform_accesses / 100,
                    activity_completion,
                    study_hours_per_week / 20,
                ]
            ],
            dtype=torch.float32,
        )

        with torch.no_grad():
            prediction = self.model(features)

        return round(float(prediction.item()), 4)


@lru_cache(maxsize=1)
def get_predictor():
    return DropoutPredictor()