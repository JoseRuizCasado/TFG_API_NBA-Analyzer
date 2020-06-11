from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('teams/', ListTeams.as_view(), name='list-all-teams'),
    path('team/<int:team_id>', GetTeamById.as_view(), name='get-team-by-id'),
    path('team/<str:team_abbreviation>', GetTeamByAbbreviation.as_view(), name='get-team-by-abbreviation'),
    path('create-team/', CreateTeam.as_view(), name='create-team'),
    path('update-team/<int:team_id>', UpdateTeam.as_view(), name='update-team'),
    path('players-from-team/<int:team_id>', ListPlayersByTeamId.as_view(), name='list-players-by-team-id'),
    path('player/<int:player_id>', GetPlayerById.as_view(), name='get-players-by-ig'),
    path('create-player/', CreatePlayer.as_view(), name='create-player'),
    path('update-player/<int:player_id>', UpdatePlayer.as_view(), name='update-player'),
    path('game/<str:game_id>', GetGameById.as_view(), name='get-game-by-id'),
    path('game-by-local-team/<int:local_team_id>', ListGamesByLocalTeamId.as_view(), name='get-game-by-local-team-id'),
    path('game-by-visitor-team/<int:visitor_team_id>', ListGamesByVisitorTeamId.as_view(),
         name='get-game-by-visitor-team-id'),
    path('game-by-winner-team/<int:winner_team_id>', ListGamesByWinnerTeamId.as_view(),
         name='get-game-by-winner-team-id'),
    path('team-games/<int:team_id>', ListTeamGames.as_view(), name='team-games'),
    path('create-game/', CreateGame.as_view(), name='create-game')
]

urlpatterns = format_suffix_patterns(urlpatterns)
