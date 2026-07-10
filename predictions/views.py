from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DropoutPredictionSerializer
from .services import get_predictor


def classify_risk(probability):
    if probability < 0.30:
        return {
            "level": "low",
            "label": "Baixo",
            "message": (
                "O estudante apresenta baixo risco estimado de evasão."
            ),
        }

    if probability < 0.60:
        return {
            "level": "medium",
            "label": "Médio",
            "message": (
                "O estudante merece acompanhamento preventivo."
            ),
        }

    return {
        "level": "high",
        "label": "Alto",
        "message": (
            "O estudante apresenta sinais que indicam necessidade "
            "de acompanhamento prioritário."
        ),
    }


class DropoutPredictionView(APIView):
    def post(self, request):
        serializer = DropoutPredictionSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        try:
            predictor = get_predictor()

            probability = predictor.predict(
                **serializer.validated_data
            )
        except FileNotFoundError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        risk = classify_risk(probability)

        return Response(
            {
                "dropout_probability": probability,
                "dropout_percentage": round(
                    probability * 100,
                    2,
                ),
                "risk_level": risk["level"],
                "risk_label": risk["label"],
                "message": risk["message"],
                "model": "PyTorch neural network",
                "disclaimer": (
                    "Resultado demonstrativo baseado em dados "
                    "sintéticos. Não deve ser usado isoladamente "
                    "em decisões acadêmicas reais."
                ),
            },
            status=status.HTTP_200_OK,
        )