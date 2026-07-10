from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StudentMetricViewSet, StudentViewSet

router = DefaultRouter()
router.register("students", StudentViewSet, basename="student")
router.register("metrics", StudentMetricViewSet, basename="student-metric")

urlpatterns = [
    path("", include(router.urls)),
]