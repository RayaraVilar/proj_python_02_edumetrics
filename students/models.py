from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    course = models.CharField(max_length=120)
    semester = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StudentMetric(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="metrics",
    )
    attendance_rate = models.FloatField()
    average_grade = models.FloatField()
    platform_accesses = models.PositiveIntegerField(default=0)
    completed_activities = models.PositiveIntegerField(default=0)
    total_activities = models.PositiveIntegerField(default=0)
    study_hours_per_week = models.FloatField(default=0)
    dropout_risk = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Métricas de {self.student.name}"