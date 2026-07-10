import pandas as pd

from students.models import StudentMetric


def build_students_dataframe():
    queryset = StudentMetric.objects.select_related("student").values(
        "student_id",
        "student__name",
        "student__course",
        "student__semester",
        "attendance_rate",
        "average_grade",
        "platform_accesses",
        "completed_activities",
        "total_activities",
        "study_hours_per_week",
        "dropout_risk",
    )

    return pd.DataFrame(list(queryset))


def classify_risk(dropout_risk):
    if dropout_risk < 0.30:
        return "low"

    if dropout_risk < 0.60:
        return "medium"

    return "high"


def generate_general_summary():
    dataframe = build_students_dataframe()

    if dataframe.empty:
        return {
            "total_students": 0,
            "average_attendance": 0,
            "average_grade": 0,
            "average_dropout_risk": 0,
            "risk_distribution": {
                "low": 0,
                "medium": 0,
                "high": 0,
            },
            "students_by_course": [],
            "highest_risk_students": [],
        }

    dataframe["risk_level"] = dataframe[
        "dropout_risk"
    ].apply(classify_risk)

    risk_counts = (
        dataframe["risk_level"]
        .value_counts()
        .to_dict()
    )

    students_by_course = (
        dataframe.groupby("student__course")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="total")
        .rename(columns={"student__course": "course"})
        .to_dict(orient="records")
    )

    highest_risk_students = (
        dataframe.sort_values(
            by="dropout_risk",
            ascending=False,
        )
        .head(5)[
            [
                "student_id",
                "student__name",
                "student__course",
                "attendance_rate",
                "average_grade",
                "dropout_risk",
                "risk_level",
            ]
        ]
        .rename(
            columns={
                "student_id": "id",
                "student__name": "name",
                "student__course": "course",
            }
        )
        .to_dict(orient="records")
    )

    return {
        "total_students": int(len(dataframe)),
        "average_attendance": round(
            float(dataframe["attendance_rate"].mean()),
            2,
        ),
        "average_grade": round(
            float(dataframe["average_grade"].mean()),
            2,
        ),
        "average_dropout_risk": round(
            float(dataframe["dropout_risk"].mean()),
            4,
        ),
        "risk_distribution": {
            "low": int(risk_counts.get("low", 0)),
            "medium": int(risk_counts.get("medium", 0)),
            "high": int(risk_counts.get("high", 0)),
        },
        "students_by_course": students_by_course,
        "highest_risk_students": highest_risk_students,
    }