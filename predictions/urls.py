from django.urls import path

from .views import DropoutPredictionView


app_name = "predictions"

urlpatterns = [
    path(
        "dropout-risk/",
        DropoutPredictionView.as_view(),
        name="dropout-risk",
    ),
]