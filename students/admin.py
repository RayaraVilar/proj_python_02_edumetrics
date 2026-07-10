from django.contrib import admin

from .models import Student, StudentMetric


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "course",
        "semester",
        "created_at",
    )
    search_fields = ("name", "email", "course")
    list_filter = ("course", "semester")


@admin.register(StudentMetric)
class StudentMetricAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "attendance_rate",
        "average_grade",
        "platform_accesses",
        "dropout_risk",
        "updated_at",
    )
    search_fields = ("student__name", "student__email")