from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import generate_general_summary


class GeneralAnalyticsView(APIView):
    def get(self, request):
        summary = generate_general_summary()

        return Response(summary)