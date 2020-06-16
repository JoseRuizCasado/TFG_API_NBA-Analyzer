from rest_framework import views, response
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
            return response.Response({'success': 'Game info is already loaded on the system'})
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

        requests.put(url=f'http://127.0.0.1:8000/dbmanager/update-game/{game_id}',
                     json={'game': {'information_loaded': True}})

        return response.Response({'success': f'Game {game_json["game_id"]} files analyzed successfully',
                                  'local_team': home_team_statistics,
                                  'visitor_team': visitor_team_statistics})
