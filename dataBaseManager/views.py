from django.db.models import Q
from rest_framework import views, response
from .models import Team, Player, Game
from .serializer import TeamSerializer, PlayerSerializer, GameSerializer


# Create your views here.


class ListTeams(views.APIView):
    """
        Get list of all Teams stored in the database
    """

    @staticmethod
    def get(request):
        data = []
        teams = Team.objects.all()
        # Transform team objects into JSON format
        serializer = TeamSerializer(teams, many=True)
        return response.Response({'teams': serializer.data})


class GetTeamById(views.APIView):
    """
        Get the Team with selected id
    """

    @staticmethod
    def get(request, team_id, format=None):
        team = Team.objects.get(team_id=team_id)
        # Transform team object into JSON format
        serializer = TeamSerializer(team)
        return response.Response({'team': serializer.data})


class GetTeamByAbbreviation(views.APIView):
    """
        Get the Team with selected abbreviation
    """

    @staticmethod
    def get(request, team_abbreviation, format=None):
        team = Team.objects.get(abbreviation=team_abbreviation)
        # Transform team object into JSON format
        serializer = TeamSerializer(team)
        return response.Response({'team': serializer.data})


class CreateTeam(views.APIView):
    """
        Create Team in the database with the request's body information
    """

    @staticmethod
    def post(request):
        team = request.data.get('team')
        # Create the team from the request data
        serializer = TeamSerializer(data=team)
        if serializer.is_valid(raise_exception=True):
            saved_team = serializer.save()
        return response.Response({'success': f'Team {saved_team.team_id} created successfully'})


class UpdateTeam(views.APIView):
    """
        Update the Team info with the included information in the request
    """

    @staticmethod
    def put(request, team_id):
        saved_team = Team.objects.get(team_id=team_id)
        data = request.data.get('team')
        # Add info to team instance and save it in the database
        serializer = TeamSerializer(instance=saved_team, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_team = serializer.save()
        return response.Response({'success': f'Team {saved_team.team_id} updated successfully'})


class ListPlayersByTeamId(views.APIView):
    """
        Get the player's list of selected team
    """

    @staticmethod
    def get(request, team_id):
        players = Player.objects.all().filter(team_id=team_id)
        # Transform Players objects into JSON format
        serializer = PlayerSerializer(players, many=True)
        return response.Response({'players': serializer.data})


class GetPlayerById(views.APIView):
    """
        Get player by id
    """

    @staticmethod
    def get(self, player_id):
        player = Player.objects.get(player_id=player_id)
        # Transform Player object into JSON format
        serializer = PlayerSerializer(player)
        return response.Response({'player': serializer.data})


class CreatePlayer(views.APIView):
    """
        Create Player in the database with the request's body information
    """

    @staticmethod
    def post(request):
        player = request.data.get('player')
        # Create the team from the request data
        serializer = PlayerSerializer(data=player)
        if serializer.is_valid(raise_exception=True):
            saved_player = serializer.save()
        return response.Response({'success': f'Player {saved_player.player_id} created successfully'})


class UpdatePlayer(views.APIView):
    """
        Update the Player info with the included information in the request
    """

    @staticmethod
    def put(request, player_id):
        saved_player = Player.objects.get(player_id=player_id)
        data = request.data.get('player')
        # Add info to team instance and save it in the database
        serializer = PlayerSerializer(instance=saved_player, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_player = serializer.save()
        return response.Response({'success': f'Player {saved_player.player_id} updated successfully'})


class GetGameById(views.APIView):
    """
        Get Game by id
    """

    @staticmethod
    def get(request, game_id):
        game = Game.objects.get(game_id=game_id)
        # Transform game object into JSON format
        serializer = GameSerializer(game)
        return response.Response({'game': serializer.data})


class ListGamesByLocalTeamId(views.APIView):
    """
        List Game by local team id
    """

    @staticmethod
    def get(request, local_team_id):
        games = Game.objects.filter(local_team=local_team_id)
        # Transform game object into JSON format
        serializer = GameSerializer(games, many=True)
        return response.Response({'games': serializer.data})


class ListGamesByVisitorTeamId(views.APIView):
    """
        List Game by visitor team id
    """

    @staticmethod
    def get(request, visitor_team_id):
        games = Game.objects.filter(visitor_team_id=visitor_team_id)
        # Transform game object into JSON format
        serializer = GameSerializer(games, many=True)
        return response.Response({'games': serializer.data})


class ListGamesByWinnerTeamId(views.APIView):
    """
        List Game by winner team id
    """

    @staticmethod
    def get(request, winner_team_id):
        games = Game.objects.filter(winner_team_id=winner_team_id)
        # Transform game object into JSON format
        serializer = GameSerializer(games, many=True)
        return response.Response({'games': serializer.data})


class ListTeamGames(views.APIView):
    """
        List all Team's Games
    """

    @staticmethod
    def get(request, team_id):
        games = Game.objects.filter(Q(local_team=team_id) | Q(visitor_team=team_id))
        # Transform game objects into JSON format
        serializer = GameSerializer(games, many=True)
        return response.Response({'games': serializer.data})


class CreateGame(views.APIView):
    """
        Create Game in the database with the request's body information
    """

    @staticmethod
    def post(request):
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
        saved_game = Game.objects.get(game_id=game_id)
        data = request.data.get('game')
        # Add info to team instance and save it in the database
        serializer = GameSerializer(instance=saved_game, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_player = serializer.save()
        return response.Response({'success': f'Game {saved_game.game_id} updated successfully'})
