from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', PredictGame.as_view(), name='predict-game'),
    path('/predict-player-cluster/<str:position>', PredictGame.as_view(), name='predict-player-cluster')
]

urlpatterns = format_suffix_patterns(urlpatterns)
