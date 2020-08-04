from rest_framework import views, response, status
import requests
from .StatsCalculator import *


class GetTeamStats(views.APIView):

    @staticmethod
    def get(request, team_id):
        """
        Get advanced stats for the Team given in the url
        :param request:
        :param team_id:  Team numerical id
        :return: Team stats formatted as JSON
        """
        # Get Team stats stored in database
        team_json = requests.get(url=f'http://127.0.0.1:8000/dbmanager/team/{team_id}').json()['team']
        # Calculate advanced stats with stats from de database
        team_json['TmOffRtg'] = team_off_rtg(team_json['scored_points'], team_json['field_goals_attempts'],
                                             team_json['field_goals_made'], team_json['turnovers'],
                                             team_json['free_throws_attempts'],
                                             team_json['offensive_rebounds'], team_json['conceded_defensive_rebounds'])
        team_json['TmFloor%'] = team_floor_per(team_json['field_goals_attempts'],
                                               team_json['field_goals_made'], team_json['turnovers'],
                                               team_json['free_throws_attempts'], team_json['free_throws_made'],
                                               team_json['offensive_rebounds'],
                                               team_json['conceded_defensive_rebounds'])
        team_json['DefRtg'] = team_def_rtg(team_json['conceded_points'], team_json['field_goals_attempts'],
                                           team_json['field_goals_made'], team_json['turnovers'],
                                           team_json['free_throws_attempts'],
                                           team_json['offensive_rebounds'], team_json['conceded_defensive_rebounds'])
        team_json['NetRtg'] = team_json['TmOffRtg'] - team_json['DefRtg']
        team_json['Pace'] = team_pace((team_json['played_minutes'] / 60), team_json['field_goals_attempts'],
                                      team_json['field_goals_made'], team_json['turnovers'],
                                      team_json['free_throws_attempts'], team_json['offensive_rebounds'],
                                      team_json['conceded_defensive_rebounds'],
                                      team_json['conceded_field_goals_attempts'],
                                      team_json['conceded_field_goals_made'], team_json['conceded_turnovers'],
                                      team_json['conceded_free_throws_attempts'],
                                      team_json['conceded_offensive_rebounds'],
                                      team_json['defensive_rebounds'])
        team_json['TS%'] = true_shooting_per(team_json['scored_points'], team_json['field_goals_attempts'],
                                             team_json['free_throws_attempts'])
        two_field_goals = team_json['field_goals_made'] - team_json['three_points_field_goals_made']
        team_json['eFG%'] = effective_field_goals_per(two_field_goals, team_json['three_points_field_goals_made'],
                                                      team_json['field_goals_attempts'])
        team_json['FTARate'] = free_throws_att_rate(team_json['free_throws_attempts'],
                                                    team_json['field_goals_attempts'])
        team_json['3FGARate'] = three_field_goals_att_rate(team_json['three_points_field_goals_attempts'],
                                                           team_json['field_goals_attempts'])
        team_json['TmOR%'] = team_off_rebound_per(team_json['offensive_rebounds'],
                                                  team_json['conceded_defensive_rebounds'])
        team_json['TmDR%'] = team_def_rebound_per(team_json['defensive_rebounds'],
                                                  team_json['conceded_offensive_rebounds'])
        team_json['BLK%'] = team_blocks_per(team_json['blocks'], team_json['conceded_field_goals_attempts'],
                                            team_json['conceded_three_points_field_goals_attempts'])
        team_json['TOV%'] = turnovers_per(team_json['turnovers'], team_json['field_goals_attempts'],
                                          team_json['free_throws_attempts'])
        team_json['AST%'] = team_assists_per(team_json['assists'], team_json['field_goals_attempts'])
        team_json['STL%'] = team_steals_per(team_json['steals'], team_json['conceded_field_goals_attempts'],
                                            team_json['conceded_field_goals_made'], team_json['conceded_turnovers'],
                                            team_json['conceded_free_throws_attempts'],
                                            team_json['conceded_offensive_rebounds'],
                                            team_json['defensive_rebounds'])

        return response.Response(data={'team': team_json}, status=status.HTTP_200_OK)


class GetTeamPlayersStats(views.APIView):

    @staticmethod
    def get(request, team_id):
        """
        Get Team and Players advanced stats
        :param request:
        :param team_id: Team numerical id
        :return: Team stats formatted as JSON
        """
        # Get Team stats stored in database
        team_json = requests.get(url=f'http://127.0.0.1:8000/dbmanager/team/{team_id}').json()['team']
        # Calculate advanced stats with stats from de database
        team_json['TmOffRtg'] = team_off_rtg(team_json['scored_points'], team_json['field_goals_attempts'],
                                             team_json['field_goals_made'], team_json['turnovers'],
                                             team_json['free_throws_attempts'],
                                             team_json['offensive_rebounds'], team_json['conceded_defensive_rebounds'])
        team_json['TmFloor%'] = team_floor_per(team_json['field_goals_attempts'],
                                               team_json['field_goals_made'], team_json['turnovers'],
                                               team_json['free_throws_attempts'], team_json['free_throws_made'],
                                               team_json['offensive_rebounds'],
                                               team_json['conceded_defensive_rebounds'])
        team_json['DefRtg'] = team_def_rtg(team_json['conceded_points'], team_json['field_goals_attempts'],
                                           team_json['field_goals_made'], team_json['turnovers'],
                                           team_json['free_throws_attempts'],
                                           team_json['offensive_rebounds'], team_json['conceded_defensive_rebounds'])
        team_json['NetRtg'] = team_json['TmOffRtg'] - team_json['DefRtg']
        team_json['Pace'] = team_pace((team_json['played_minutes'] / 60), team_json['field_goals_attempts'],
                                      team_json['field_goals_made'], team_json['turnovers'],
                                      team_json['free_throws_attempts'], team_json['offensive_rebounds'],
                                      team_json['conceded_defensive_rebounds'],
                                      team_json['conceded_field_goals_attempts'],
                                      team_json['conceded_field_goals_made'], team_json['conceded_turnovers'],
                                      team_json['conceded_free_throws_attempts'],
                                      team_json['conceded_offensive_rebounds'],
                                      team_json['defensive_rebounds']
                                      )
        team_json['TS%'] = true_shooting_per(team_json['scored_points'], team_json['field_goals_attempts'],
                                             team_json['free_throws_attempts'])
        two_field_goals = team_json['field_goals_made'] - team_json['three_points_field_goals_made']
        team_json['eFG%'] = effective_field_goals_per(two_field_goals, team_json['three_points_field_goals_made'],
                                                      team_json['field_goals_attempts'])
        team_json['FTARate'] = free_throws_att_rate(team_json['free_throws_attempts'],
                                                    team_json['field_goals_attempts'])
        team_json['3FGARate'] = three_field_goals_att_rate(team_json['three_points_field_goals_attempts'],
                                                           team_json['field_goals_attempts'])
        team_json['TmOR%'] = team_off_rebound_per(team_json['offensive_rebounds'],
                                                  team_json['conceded_defensive_rebounds'])
        team_json['TmDR%'] = team_def_rebound_per(team_json['defensive_rebounds'],
                                                  team_json['conceded_offensive_rebounds'])
        team_json['BLK%'] = team_blocks_per(team_json['blocks'], team_json['conceded_field_goals_attempts'],
                                            team_json['conceded_three_points_field_goals_attempts'])
        team_json['TOV%'] = turnovers_per(team_json['turnovers'], team_json['field_goals_attempts'],
                                          team_json['free_throws_attempts'])
        team_json['AST%'] = team_assists_per(team_json['assists'], team_json['field_goals_attempts'])
        team_json['STL%'] = team_steals_per(team_json['steals'], team_json['conceded_field_goals_attempts'],
                                            team_json['conceded_field_goals_made'], team_json['conceded_turnovers'],
                                            team_json['conceded_free_throws_attempts'],
                                            team_json['conceded_offensive_rebounds'],
                                            team_json['defensive_rebounds'])

        # Load team players
        players_json = requests.get(url=f'http://127.0.0.1:8000/dbmanager/players-from-team/{team_id}').json()
        players_list = players_json['players']

        for player in players_list:
            try:
                free_throws_per = team_json['free_throws_made'] / team_json['free_throws_attempts']
            except:
                free_throws_per = 0

            player['OffRtg'], player['Floor%'] = player_off_rtg_floor_per(player['scored_points'],
                                                                          (player['played_minutes'] / 60),
                                                                          player['field_goals_made'],
                                                                          player['field_goals_attempts'],
                                                                          player['three_points_field_goals_made'],
                                                                          player['free_throws_made'],
                                                                          player['free_throws_attempts'],
                                                                          free_throws_per,
                                                                          player['offensive_rebounds'],
                                                                          player['assists'],
                                                                          player['turnovers'],
                                                                          team_json['scored_points'],
                                                                          (team_json['played_minutes'] / 60) * 5,
                                                                          team_json['field_goals_made'],
                                                                          team_json['field_goals_attempts'],
                                                                          team_json['three_points_field_goals_made'],
                                                                          team_json['free_throws_made'],
                                                                          team_json['free_throws_attempts'],
                                                                          free_throws_per,
                                                                          team_json['offensive_rebounds'],
                                                                          team_json['assists'],
                                                                          team_json['turnovers'],
                                                                          team_json['TmOR%'] / 100)
            player['DefRtg'] = player_def_rtg((player['played_minutes'] / 60), player['defensive_rebounds'],
                                              player['steals'], player['blocks'], player['personal_fouls'],
                                              (team_json['played_minutes'] / 60) * 5,
                                              team_json['field_goals_made'], team_json['field_goals_attempts'],
                                              team_json['defensive_rebounds'], team_json['blocks'],
                                              team_json['turnovers'], team_json['free_throws_attempts'],
                                              team_json['offensive_rebounds'], team_json['steals'],
                                              team_json['personal_fouls'], team_json['DefRtg'],
                                              team_json['conceded_points'], team_json['conceded_field_goals_made'],
                                              team_json['conceded_field_goals_attempts'],
                                              team_json['conceded_free_throws_made'],
                                              team_json['conceded_free_throws_attempts'],
                                              team_json['conceded_offensive_rebounds'],
                                              team_json['conceded_defensive_rebounds'], team_json['conceded_turnovers'])
            player['NetRtg'] = player['OffRtg'] - player['DefRtg']
            player['TS%'] = true_shooting_per(player['scored_points'], player['field_goals_attempts'],
                                              player['free_throws_attempts'])
            player['eFG%'] = \
                effective_field_goals_per(player['field_goals_made'] - player['three_points_field_goals_made'],
                                          player['three_points_field_goals_made'], player['field_goals_attempts'])
            player['FTARate'] = free_throws_att_rate(player['free_throws_attempts'], player['field_goals_attempts'])
            player['3FGARate'] = three_field_goals_att_rate(player['three_points_field_goals_made'],
                                                            player['field_goals_attempts'])
            player['OR%'] = player_off_rebound_per((player['played_minutes'] / 60), player['offensive_rebounds'],
                                                   (team_json['played_minutes'] / 60) * 5,
                                                   team_json['offensive_rebounds'],
                                                   team_json['conceded_defensive_rebounds'])
            player['DR%'] = player_def_rebound_per((player['played_minutes'] / 60), player['defensive_rebounds'],
                                                   (team_json['played_minutes'] / 60) * 5,
                                                   team_json['defensive_rebounds'],
                                                   team_json['conceded_offensive_rebounds'])
            player['BLK%'] = player_blocks_per((player['played_minutes'] / 60), player['blocks'],
                                               (team_json['played_minutes'] / 60) * 5,
                                               team_json['conceded_field_goals_attempts'],
                                               team_json['conceded_three_points_field_goals_attempts'])
            player['TOV%'] = turnovers_per(player['turnovers'], player['field_goals_attempts'],
                                           player['free_throws_attempts'])
            player['AST%'] = player_assists_per((player['played_minutes'] / 60), player['field_goals_made'],
                                                player['assists'], (team_json['played_minutes'] / 60) * 5,
                                                team_json['field_goals_made'])
            player['STL%'] = player_steals_per((player['played_minutes'] / 60), player['steals'],
                                               (team_json['played_minutes'] / 60) * 5,
                                               team_json['conceded_field_goals_attempts'],
                                               team_json['conceded_field_goals_made'], team_json['conceded_turnovers'],
                                               team_json['conceded_free_throws_attempts'],
                                               team_json['conceded_offensive_rebounds'],
                                               team_json['defensive_rebounds'])
            player['USG%'] = usage_per((player['played_minutes'] / 60), player['field_goals_attempts'],
                                       player['free_throws_attempts'], player['turnovers'],
                                       (team_json['played_minutes'] / 60) * 5, team_json['field_goals_attempts'],
                                       team_json['free_throws_attempts'], team_json['turnovers'])

        team_json['players'] = players_list
        return response.Response(data={'team': team_json}, status=status.HTTP_200_OK)
