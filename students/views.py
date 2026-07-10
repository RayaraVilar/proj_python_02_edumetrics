from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Student, StudentMetric
from .serializers import StudentMetricSerializer, StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("metrics").all()
    serializer_class = StudentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["course", "semester"]
    search_fields = ["name", "email", "course"]
    ordering_fields = ["name", "semester", "created_at"]
    ordering = ["name"]


class StudentMetricViewSet(viewsets.ModelViewSet):
    queryset = StudentMetric.objects.select_related("student").all()
    serializer_class = StudentMetricSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ["student"]
    ordering_fields = [
        "attendance_rate",
        "average_grade",
        "dropout_risk",
        "updated_at",
    ]