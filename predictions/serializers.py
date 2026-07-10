from rest_framework import serializers


class DropoutPredictionSerializer(serializers.Serializer):
    attendance_rate = serializers.FloatField(
        min_value=0,
        max_value=100,
    )
    average_grade = serializers.FloatField(
        min_value=0,
        max_value=10,
    )
    platform_accesses = serializers.IntegerField(
        min_value=0,
    )
    completed_activities = serializers.IntegerField(
        min_value=0,
    )
    total_activities = serializers.IntegerField(
        min_value=0,
    )
    study_hours_per_week = serializers.FloatField(
        min_value=0,
    )

    def validate(self, attrs):
        completed = attrs["completed_activities"]
        total = attrs["total_activities"]

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