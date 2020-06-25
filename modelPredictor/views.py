from django.shortcuts import render
from .apps import ModelpredictorConfig
from rest_framework import views, response, status


class PredictGame(views.APIView):

    @staticmethod
    def get(request):
        return response.Response(status=status.HTTP_200_OK)
