from django.urls import path

from .views import GeneralAnalyticsView

urlpatterns = [
    path(
        "summary/",
        GeneralAnalyticsView.as_view(),
        name="analytics-summary",
    ),
]