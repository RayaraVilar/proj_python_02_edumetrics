from django.urls import path

from .views import dashboard_home, prediction_page


app_name = "dashboard"

urlpatterns = [
    path("", dashboard_home, name="home"),
    path(
        "predicao/",
        prediction_page,
        name="prediction",
    ),
]