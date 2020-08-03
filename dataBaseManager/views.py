from django.db.models import Q
from rest_framework import views, response
from .models import Team, Player, Game, DefendInfo
from .serializer import TeamSerializer, PlayerSerializer, GameSerializer, DefendInfoSerializer


# Create your views here.


class ListTeams(views.APIView):

    @staticmethod
    def get(request):
        """
         Get list of all Teams stored in the database

         :return: List of Teams, each Team formatted as JSON
         """
        teams = Team.objects.all()
        # Transform team objects into JSON format
        serializer = TeamSerializer(teams, many=True)
        return response.Response({'teams': serializer.data})


class GetTeamById(views.APIView):

    @staticmethod
    def get(request, team_id, format=None):
        """
        Get the Team with selected id
        :param request:
        :param team_id: Team numerical id
        :return: Team formatted as JSON
        """
        team = Team.objects.get(team_id=team_id)
        # Transform team object into JSON format
        serializer = TeamSerializer(team)
        return response.Response({'team': serializer.data})


class GetTeamByAbbreviation(views.APIView):

    @staticmethod
    def get(request, team_abbreviation, format=None):
        """
        Get the Team with selected abbreviation
        :param request:
        :param team_abbreviation: Team abbreviation
        :return: Team formatted as JSON
        """
        team = Team.objects.get(abbreviation=team_abbreviation)
        # Transform team object into JSON format
        serializer = TeamSerializer(team)
        return response.Response({'team': serializer.data})


class CreateTeam(views.APIView):

    @staticmethod
    def post(request):
        """
        Create Team in the database with the request's body information
        :param request: Request with Team data as JSON
        :return: Response with the success of the request
        """
        team = request.data.get('team')
        # Create the team from the request data
        serializer = TeamSerializer(data=team)
        if serializer.is_valid(raise_exception=True):
            saved_team = serializer.save()
        return response.Response({'success': f'Team {saved_team.team_id} created successfully'})


class UpdateTeam(views.APIView):

    @staticmethod
    def put(request, team_id):
        """
        Update the Team info with the included information in the request
        :param request: Request with Team data as JSON
        :param team_id: Team numerical id
        :return: Response with the success of the request
        """
        saved_team = Team.objects.get(team_id=team_id)
        data = request.data.get('team')
        # Add info to team instance and save it in the database
        serializer = TeamSerializer(instance=saved_team, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_team = serializer.save()
        return response.Response({'success': f'Team {saved_team.team_id} updated successfully'})


class ListPlayersByTeamId(views.APIView):

    @staticmethod
    def get(request, team_id):
        """
        Get the player's list of selected team
        :param request:
        :param team_id: Team numerical id
        :return: List of Players, each Player formatted as JSON
        """
        players = Player.objects.all().filter(team_id=team_id)
        # Transform Players objects into JSON format
        serializer = PlayerSerializer(players, many=True)
        return response.Response({'players': serializer.data})


class GetPlayerById(views.APIView):

    @staticmethod
    def get(request, player_id):
        """

        :param request:
        :param player_id: Player numerical id
        :return:
        """
        player = Player.objects.get(player_id=player_id)
        # Transform Player object into JSON format
        serializer = PlayerSerializer(player)
        return response.Response({'player': serializer.data})


class CreatePlayer(views.APIView):

    @staticmethod
    def post(request):
        """
        Create Player in the database with the request's body information
        :param request: Request with Player data as JSON
        :return: Response with the success of the request
        """
        player = request.data.get('player')
        # Create the team from the request data
        serializer = PlayerSerializer(data=player)
        if serializer.is_valid(raise_exception=True):
            saved_player = serializer.save()
        return response.Response({'success': f'Player {saved_player.player_id} created successfully'})


class UpdatePlayer(views.APIView):

    @staticmethod
    def put(request, player_id):
        """
        Update the Player info with the included information in the request
        :param request:
        :param player_id: Player numerical id
        :return: Response with the success of the request
        """
        saved_player = Player.objects.get(player_id=player_id)
        data = request.data.get('player')
        # Add info to team instance and save it in the database
        serializer = PlayerSerializer(instance=saved_player, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_player = serializer.save()
        return response.Response({'success': f'Player {saved_player.player_id} updated successfully'})


class GetGameById(views.APIView):
    @staticmethod
    def get(request, game_id):
        """
        Get Game by id
        :param request:
        :param game_id: Game numerical id
        :return: Game formatted as JSON
        """
        game = Game.objects.get(game_id=game_id)
        # Transform game object into JSON format
        serializer = GameSerializer(game)
        return response.Response({'game': serializer.data})


class ListGamesByLocalTeamId(views.APIView):

    @staticmethod
    def get(request, local_team_id):
        """
        List Game by local team id
        :param request:
        :param local_team_id: Local Team numerical id
        :return: Lists of Games, each one formatted as JSON
        """
        games = Game.objects.filter(local_team=local_team_id)
        # Transform game object into JSON format
        serializer = GameSerializer(games, many=True)
        return response.Response({'games': serializer.data})


class ListGamesByVisitorTeamId(views.APIView):

    @staticmethod
    def get(request, visitor_team_id):
        """
        List Game by visitor team id
        :param request:
        :param visitor_team_id: Visitor Team numerical id
        :return: Lists of Games, each one formatted as JSON
        """
        games = Game.objects.filter(visitor_team_id=visitor_team_id)
        # Transform game object into JSON format
        serializer = GameSerializer(games, many=True)
        return response.Response({'games': serializer.data})


class ListGamesByWinnerTeamId(views.APIView):

    @staticmethod
    def get(request, winner_team_id):
        """
        List Game by winner team id
        :param request:
        :param winner_team_id: Winner Team numerical id
        :return: Lists of Games, each one formatted as JSON
        """
        games = Game.objects.filter(winner_team_id=winner_team_id)
        # Transform game object into JSON format
        serializer = GameSerializer(games, many=True)
        return response.Response({'games': serializer.data})


class ListTeamGames(views.APIView):

    @staticmethod
    def get(request, team_id):
        """
        List all Team's Games
        :param request:
        :param team_id: Team numerical id
        :return: List of Games, each Game formatted as JSON
        """
        games = Game.objects.filter(Q(local_team=team_id) | Q(visitor_team=team_id))
        # Transform game objects into JSON format
        serializer = GameSerializer(games, many=True)
        return response.Response({'games': serializer.data})


class CreateGame(views.APIView):

    @staticmethod
    def post(request):
        """
        Create Game in the database with the request's body information
        :param request: Request with Game data as JSON
        :return: Response with the success of the request
        """
        game = request.data.get('game')
        # Create the team from the request data
        serializer = GameSerializer(data=game)
        if serializer.is_valid(raise_exception=True):
            saved_game = serializer.save()
        return response.Response({'success': f'Game {saved_game.game_id} created successfully'})


class UpdateGame(views.APIView):
    """
        Update the Game info with the included information in the request
    """

    @staticmethod
    def put(request, game_id):
        """
        Update the Game info with the included information in the request
        :param request: Request with Game data as JSON
        :param game_id: Game string id
        :return: Response with the success of the request
        """
        saved_game = Game.objects.get(game_id=game_id)
        data = request.data.get('game')
        # Add info to team instance and save it in the database
        serializer = GameSerializer(instance=saved_game, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_game = serializer.save()
        return response.Response({'success': f'Game {saved_game.game_id} updated successfully'})


class CreateDefendInfo(views.APIView):

    @staticmethod
    def post(request):
        data = request.data.get('data')
        serializer = DefendInfoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            saved_data = serializer.save()
        return response.Response({'success': f'Shooter {saved_data.shooter_id} and defender {saved_data.defender_id} '
                                             f'info created successfully'})
