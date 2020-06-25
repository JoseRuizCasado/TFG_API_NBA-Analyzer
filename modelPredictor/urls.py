from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', PredictGame.as_view(), name='predict-game')
]

urlpatterns = format_suffix_patterns(urlpatterns)
