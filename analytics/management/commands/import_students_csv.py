from pathlib import Path

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from predictions.services import get_predictor
from students.models import Student, StudentMetric

class Command(BaseCommand):
    help = "Importa estudantes e métricas acadêmicas a partir de um CSV."

    required_columns = {
        "name",
        "email",
        "age",
        "course",
        "semester",
        "attendance_rate",
        "average_grade",
        "platform_accesses",
        "completed_activities",
        "total_activities",
        "study_hours_per_week",
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            type=str,
            help="Caminho do arquivo CSV.",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])

        if not csv_path.exists():
            raise CommandError(
                f"Arquivo não encontrado: {csv_path}"
            )

        try:
            dataframe = pd.read_csv(csv_path)
        except Exception as error:
            raise CommandError(
                f"Não foi possível ler o CSV: {error}"
            ) from error

        missing_columns = self.required_columns - set(dataframe.columns)

        if missing_columns:
            columns = ", ".join(sorted(missing_columns))

            raise CommandError(
                f"Colunas obrigatórias ausentes: {columns}"
            )

        dataframe = self.clean_dataframe(dataframe)
            
        dataframe = self.clean_dataframe(dataframe)

        try:
            predictor = get_predictor()
        except FileNotFoundError as error:
            raise CommandError(str(error)) from error


        created_students = 0
        updated_students = 0
        ignored_rows = 0

        with transaction.atomic():
            for index, row in dataframe.iterrows():
                try:
                    student, created = Student.objects.update_or_create(
                        email=row["email"],
                        defaults={
                            "name": row["name"],
                            "age": int(row["age"]),
                            "course": row["course"],
                            "semester": int(row["semester"]),
                        },
                    )

                    dropout_risk = predictor.predict(
                    attendance_rate=float(row["attendance_rate"]),
                    average_grade=float(row["average_grade"]),
                    platform_accesses=int(row["platform_accesses"]),
                    completed_activities=int(row["completed_activities"]),
                    total_activities=int(row["total_activities"]),
                    study_hours_per_week=float(
                        row["study_hours_per_week"]
                    ),
                )

                    StudentMetric.objects.update_or_create(
                        student=student,
                        defaults={
                            "attendance_rate": float(
                                row["attendance_rate"]
                            ),
                            "average_grade": float(
                                row["average_grade"]
                            ),
                            "platform_accesses": int(
                                row["platform_accesses"]
                            ),
                            "completed_activities": int(
                                row["completed_activities"]
                            ),
                            "total_activities": int(
                                row["total_activities"]
                            ),
                            "study_hours_per_week": float(
                                row["study_hours_per_week"]
                            ),
                            "dropout_risk": dropout_risk,
                        },
                    )

                    if created:
                        created_students += 1
                    else:
                        updated_students += 1

                except Exception as error:
                    ignored_rows += 1

                    self.stderr.write(
                        f"Linha {index + 2} ignorada: {error}"
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "\nImportação concluída.\n"
                f"Estudantes criados: {created_students}\n"
                f"Estudantes atualizados: {updated_students}\n"
                f"Linhas ignoradas: {ignored_rows}"
            )
        )

    def clean_dataframe(self, dataframe):
        dataframe = dataframe.copy()

        dataframe.columns = (
            dataframe.columns
            .str.strip()
            .str.lower()
        )

        text_columns = [
            "name",
            "email",
            "course",
        ]

        for column in text_columns:
            dataframe[column] = (
                dataframe[column]
                .astype(str)
                .str.strip()
            )

        dataframe["email"] = dataframe["email"].str.lower()

        numeric_columns = [
            "age",
            "semester",
            "attendance_rate",
            "average_grade",
            "platform_accesses",
            "completed_activities",
            "total_activities",
            "study_hours_per_week",
        ]

        for column in numeric_columns:
            dataframe[column] = pd.to_numeric(
                dataframe[column],
                errors="coerce",
            )

        dataframe = dataframe.dropna(
            subset=list(self.required_columns)
        )

        dataframe["attendance_rate"] = np.clip(
            dataframe["attendance_rate"],
            0,
            100,
        )

        dataframe["average_grade"] = np.clip(
            dataframe["average_grade"],
            0,
            10,
        )

        dataframe["study_hours_per_week"] = np.clip(
            dataframe["study_hours_per_week"],
            0,
            None,
        )

        return dataframe
