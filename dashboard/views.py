from django.shortcuts import render

from analytics.services import generate_general_summary
from predictions.services import get_predictor


def dashboard_home(request):
    summary = generate_general_summary()

    average_risk_percentage = round(
        summary["average_dropout_risk"] * 100,
        1,
    )

    context = {
        "summary": summary,
        "average_risk_percentage": average_risk_percentage,
    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )


def prediction_page(request):
    context = {
        "result": None,
        "form_data": {},
    }

    if request.method == "POST":
        try:
            form_data = {
                "attendance_rate": float(
                    request.POST.get("attendance_rate", 0)
                ),
                "average_grade": float(
                    request.POST.get("average_grade", 0)
                ),
                "platform_accesses": int(
                    request.POST.get("platform_accesses", 0)
                ),
                "completed_activities": int(
                    request.POST.get("completed_activities", 0)
                ),
                "total_activities": int(
                    request.POST.get("total_activities", 0)
                ),
                "study_hours_per_week": float(
                    request.POST.get("study_hours_per_week", 0)
                ),
            }

            context["form_data"] = form_data

            if (
                form_data["completed_activities"]
                > form_data["total_activities"]
            ):
                raise ValueError(
                    "As atividades concluídas não podem superar "
                    "o total de atividades."
                )

            predictor = get_predictor()

            probability = predictor.predict(**form_data)
            percentage = round(probability * 100, 1)

            if probability < 0.30:
                risk_level = "low"
                risk_label = "Baixo risco"
                title = "O cenário é positivo"
                message = (
                    "Os indicadores mostram um bom nível de "
                    "engajamento. Continue acompanhando o estudante "
                    "e reconhecendo sua evolução."
                )
                recommendation = (
                    "Mantenha o acompanhamento regular e incentive "
                    "a continuidade dos bons hábitos acadêmicos."
                )

            elif probability < 0.60:
                risk_level = "medium"
                risk_label = "Risco moderado"
                title = "Vale acompanhar mais de perto"
                message = (
                    "Alguns indicadores sugerem queda de engajamento. "
                    "Uma abordagem preventiva pode ajudar a evitar "
                    "dificuldades futuras."
                )
                recommendation = (
                    "Converse com o estudante, revise a rotina de "
                    "estudos e identifique possíveis obstáculos."
                )

            else:
                risk_level = "high"
                risk_label = "Alto risco"
                title = "Este estudante precisa de atenção"
                message = (
                    "Os dados indicam sinais importantes de possível "
                    "evasão. Uma ação rápida e acolhedora pode fazer "
                    "diferença."
                )
                recommendation = (
                    "Priorize um contato individual, investigue as "
                    "dificuldades e ofereça apoio acadêmico."
                )

            context["result"] = {
                "probability": probability,
                "percentage": percentage,
                "risk_level": risk_level,
                "risk_label": risk_label,
                "title": title,
                "message": message,
                "recommendation": recommendation,
            }

        except (ValueError, TypeError) as error:
            context["error"] = str(error)

        except FileNotFoundError as error:
            context["error"] = str(error)

    return render(
        request,
        "dashboard/prediction.html",
        context,
    )