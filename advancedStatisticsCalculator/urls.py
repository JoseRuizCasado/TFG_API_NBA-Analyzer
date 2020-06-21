from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('team-stats/<int:team_id>', GetTeamStats.as_view(), name='team-stats'),
    path('team-players-stats/<int:team_id>', GetTeamPlayersStats.as_view(), name='team-players-stats')
]

urlpatterns = format_suffix_patterns(urlpatterns)
