from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('analyze/<str:game_id>', AnalyzeGameById.as_view(), name='analyze-game')
]

urlpatterns = format_suffix_patterns(urlpatterns)
