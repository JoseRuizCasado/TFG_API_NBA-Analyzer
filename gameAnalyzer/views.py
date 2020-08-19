from rest_framework import views, response, status
import requests
from .gameInfoExtractor import extract_game_info


class AnalyzeGameById(views.APIView):
    @staticmethod
    def get(request, game_id):
        """
        Analyze play-by-play and tracking file for Game.
        It is necessary to create Game previously
        :param request:
        :param game_id: Game string id
        :return: response: response with extracted info
        """
        # Take game info
        game_json = requests.get(f'http://127.0.0.1:8000/dbmanager/game/{game_id}').json()['game']
        # Check if Game info is already loaded
        if game_json['information_loaded']:
            return response.Response({'success': 'Game info is already loaded on the system'}, status=status.HTTP_200_OK)
        # Take home Team players
        home_team_players = \
            requests.get(f'http://127.0.0.1:8000/dbmanager/players-from-team/{game_json["local_team"]}').json()
        # Take visitor Team players
        visitor_team_players = \
            requests.get(f'http://127.0.0.1:8000/dbmanager/players-from-team/{game_json["visitor_team"]}').json()

        # Extract info for home and visitor team
        home_team_statistics = \
            extract_game_info(game_id, game_json['local_team'], home_team_players['players'], 'HOMEDESCRIPTION')
        visitor_team_statistics = \
            extract_game_info(game_id, game_json['visitor_team'], visitor_team_players['players'], 'VISITORDESCRIPTION')

        # Game info loaded, update Game info to avoid reload the same Game
        requests.put(url=f'http://127.0.0.1:8000/dbmanager/update-game/{game_id}',
                     json={'game': {'information_loaded': True}})

        # Add conceded statistics to both Teams
        home_team_statistics['conceded_points'] = visitor_team_statistics['scored_points']
        home_team_statistics['conceded_field_goals_made'] = visitor_team_statistics['field_goals_made']
        home_team_statistics['conceded_field_goals_miss'] = visitor_team_statistics['field_goals_miss']
        home_team_statistics['conceded_field_goals_attempts'] = visitor_team_statistics['field_goals_attempts']
        home_team_statistics['conceded_three_points_field_goals_made'] = \
            visitor_team_statistics['three_points_field_goals_made']
        home_team_statistics['conceded_three_points_field_goals_miss'] = \
            visitor_team_statistics['three_points_field_goals_miss']
        home_team_statistics['conceded_three_points_field_goals_attempts'] = \
            visitor_team_statistics['three_points_field_goals_attempts']
        home_team_statistics['conceded_free_throws_made'] = visitor_team_statistics['free_throws_made']
        home_team_statistics['conceded_free_throws_miss'] = visitor_team_statistics['free_throws_miss']
        home_team_statistics['conceded_free_throws_attempts'] = visitor_team_statistics['free_throws_attempts']
        home_team_statistics['conceded_assists'] = visitor_team_statistics['assists']
        home_team_statistics['conceded_offensive_rebounds'] = visitor_team_statistics['offensive_rebounds']
        home_team_statistics['conceded_defensive_rebounds'] = visitor_team_statistics['defensive_rebounds']
        home_team_statistics['conceded_steals'] = visitor_team_statistics['steals']
        home_team_statistics['conceded_blocks'] = visitor_team_statistics['blocks']
        home_team_statistics['conceded_turnovers'] = visitor_team_statistics['turnovers']
        home_team_statistics['conceded_personal_fouls'] = visitor_team_statistics['personal_fouls']

        visitor_team_statistics['conceded_points'] = home_team_statistics['scored_points']
        visitor_team_statistics['conceded_field_goals_made'] = home_team_statistics['field_goals_made']
        visitor_team_statistics['conceded_field_goals_miss'] = home_team_statistics['field_goals_miss']
        visitor_team_statistics['conceded_field_goals_attempts'] = home_team_statistics['field_goals_attempts']
        visitor_team_statistics['conceded_three_points_field_goals_made'] = \
            home_team_statistics['three_points_field_goals_made']
        visitor_team_statistics['conceded_three_points_field_goals_miss'] = \
            home_team_statistics['three_points_field_goals_miss']
        visitor_team_statistics['conceded_three_points_field_goals_attempts'] = \
            home_team_statistics['three_points_field_goals_attempts']
        visitor_team_statistics['conceded_free_throws_made'] = home_team_statistics['free_throws_made']
        visitor_team_statistics['conceded_free_throws_miss'] = home_team_statistics['free_throws_miss']
        visitor_team_statistics['conceded_free_throws_attempts'] = home_team_statistics['free_throws_attempts']
        visitor_team_statistics['conceded_assists'] = home_team_statistics['assists']
        visitor_team_statistics['conceded_offensive_rebounds'] = home_team_statistics['offensive_rebounds']
        visitor_team_statistics['conceded_defensive_rebounds'] = home_team_statistics['defensive_rebounds']
        visitor_team_statistics['conceded_steals'] = home_team_statistics['steals']
        visitor_team_statistics['conceded_blocks'] = home_team_statistics['blocks']
        visitor_team_statistics['conceded_turnovers'] = home_team_statistics['turnovers']
        visitor_team_statistics['conceded_personal_fouls'] = home_team_statistics['personal_fouls']

        # Save Teams and Players stats into the database
        update_team_url = 'http://127.0.0.1:8000/dbmanager/update-team/'
        update_player_url = 'http://127.0.0.1:8000/dbmanager/update-player/'

        # Save home Team
        requests.put(url=update_team_url + f'{game_json["local_team"]}', json={'team': home_team_statistics})
        # Save visitor Team
        requests.put(url=update_team_url + f'{game_json["visitor_team"]}', json={'team': visitor_team_statistics})

        # Save home Team Players
        for home_player in home_team_statistics['players']:
            requests.put(url=update_player_url + f'{home_player["player_id"]}', json={'player': home_player})
        # Save visitor Team Players
        for visitor_player in visitor_team_statistics['players']:
            requests.put(url=update_player_url + f'{visitor_player["player_id"]}', json={'player': visitor_player})

        return response.Response(data={'success': f'Game {game_json["game_id"]} files analyzed successfully',
                                       'local_team': home_team_statistics,
                                       'visitor_team': visitor_team_statistics}, status=status.HTTP_200_OK)
