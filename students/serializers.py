from rest_framework import serializers

from .models import Student, StudentMetric


class StudentMetricSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.name",
        read_only=True,
    )

    class Meta:
        model = StudentMetric
        fields = [
            "id",
            "student",
            "student_name",
            "attendance_rate",
            "average_grade",
            "platform_accesses",
            "completed_activities",
            "total_activities",
            "study_hours_per_week",
            "dropout_risk",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "student_name",
            "updated_at",
        ]

    def validate_attendance_rate(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError(
                "A frequência deve estar entre 0 e 100."
            )
        return value

    def validate_average_grade(self, value):
        if not 0 <= value <= 10:
            raise serializers.ValidationError(
                "A média deve estar entre 0 e 10."
            )
        return value

    def validate_dropout_risk(self, value):
        if not 0 <= value <= 1:
            raise serializers.ValidationError(
                "O risco de evasão deve estar entre 0 e 1."
            )
        return value

    def validate(self, attrs):
        completed = attrs.get("completed_activities", 0)
        total = attrs.get("total_activities", 0)

        if completed > total:
            raise serializers.ValidationError(
                {
                    "completed_activities": (
                        "As atividades concluídas não podem superar "
                        "o total de atividades."
                    )
                }
            )

        return attrs


class StudentSerializer(serializers.ModelSerializer):
    metrics = StudentMetricSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "email",
            "age",
            "course",
            "semester",
            "created_at",
            "metrics",
        ]
        read_only_fields = ["id", "created_at"]