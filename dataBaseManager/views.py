from django.db.models import Q, Sum
from rest_framework import views, response, status
from .models import Team, Player, Game
from .serializer import TeamSerializer, PlayerSerializer, GameSerializer
import pandas as pd
from .apps import DatabasemanagerConfig


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
        return response.Response(data={'teams': serializer.data}, status=status.HTTP_200_OK)


class GetTeamById(views.APIView):

    @staticmethod
    def get(request, team_id):
        """
        Get the Team with selected id
        :param request:
        :param team_id: Team numerical id
        :return: Team formatted as JSON
        """
        team = Team.objects.get(team_id=team_id)
        # Transform team object into JSON format
        serializer = TeamSerializer(team)
        return response.Response(data={'team': serializer.data}, status=status.HTTP_200_OK)


class GetTeamByAbbreviation(views.APIView):

    @staticmethod
    def get(request, team_abbreviation):
        """
        Get the Team with selected abbreviation
        :param request:
        :param team_abbreviation: Team abbreviation
        :return: Team formatted as JSON
        """
        team = Team.objects.get(abbreviation=team_abbreviation)
        # Transform team object into JSON format
        serializer = TeamSerializer(team)
        return response.Response(data={'team': serializer.data}, status=status.HTTP_200_OK)


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
        return response.Response(data={'success': f'Team {saved_team.team_id} created successfully'},
                                 status=status.HTTP_200_OK)


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
        return response.Response(data={'success': f'Team {saved_team.team_id} updated successfully'},
                                 status=status.HTTP_200_OK)


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
        return response.Response(data={'players': serializer.data}, status=status.HTTP_200_OK)


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
        return response.Response(data={'player': serializer.data}, status=status.HTTP_200_OK)


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
        return response.Response(data={'success': f'Player {saved_player.player_id} created successfully'},
                                 status=status.HTTP_200_OK)


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
        return response.Response(data={'success': f'Player {saved_player.player_id} updated successfully'},
                                 status=status.HTTP_200_OK)


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
        return response.Response(data={'game': serializer.data}, status=status.HTTP_200_OK)


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
        return response.Response(data={'games': serializer.data}, status=status.HTTP_200_OK)


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
        return response.Response(data={'games': serializer.data}, status=status.HTTP_200_OK)


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
        return response.Response(data={'games': serializer.data}, status=status.HTTP_200_OK)


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
        return response.Response(data={'games': serializer.data}, status=status.HTTP_200_OK)


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
        return response.Response(data={'success': f'Game {saved_game.game_id} created successfully'},
                                 status=status.HTTP_200_OK)


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
        return response.Response(data={'success': f'Game {saved_game.game_id} updated successfully'},
                                 status=status.HTTP_200_OK)


class GetDefendInfo(views.APIView):

    @staticmethod
    def extract_defend_info(player_defend_data, position):
        shooter_cluster = 'Shooter Cluster'
        defend_success = 'Defend Success'
        player_cluster0 = player_defend_data[player_defend_data[shooter_cluster] == 0]
        count0 = player_cluster0.groupby(defend_success)[defend_success].count()
        if count0.shape[0] < 2:
            failure_cluster0 = player_cluster0[player_cluster0[defend_success] == 0]
            success_cluster0 = player_cluster0[player_cluster0[defend_success] == 1]
            if failure_cluster0.shape[0] == 0:
                count0 = count0.append(pd.Series([0], index=[0]))
            elif success_cluster0.shape[0] == 0:
                count0 = count0.append(pd.Series([0], index=[1]))
            else:
                count0 = count0.append(pd.Series([0, 0], index=[0, 1]))

        count0_json = {
            'failure': count0[0],
            'success': count0[1]
        }
        player_cluster1 = player_defend_data[player_defend_data[shooter_cluster] == 1]
        count1 = player_cluster1.groupby(defend_success)[defend_success].count()
        if count1.shape[0] < 2:
            failure_cluster1 = player_cluster1[player_cluster1[defend_success] == 0]
            success_cluster1 = player_cluster1[player_cluster1[defend_success] == 1]
            if failure_cluster1.shape[0] == 0:
                count1 = count1.append(pd.Series([0], index=[0]))
            elif success_cluster1.shape[0] == 0:
                count1 = count1.append(pd.Series([0], index=[1]))
            else:
                count1 = count1.append(pd.Series([0, 0], index=[0, 1]))

        count1_json = {
            'failure': count1[0],
            'success': count1[1]
        }
        player_cluster2 = player_defend_data[player_defend_data[shooter_cluster] == 2]
        count2 = player_cluster2.groupby(defend_success)[defend_success].count()
        if count2.shape[0] < 2:
            failure_cluster2 = player_cluster2[player_cluster2[defend_success] == 0]
            success_cluster2 = player_cluster2[player_cluster2[defend_success] == 1]
            if failure_cluster2.shape[0] == 0:
                count2 = count2.append(pd.Series([0], index=[0]))
            elif success_cluster2.shape[0] == 0:
                count2 = count2.append(pd.Series([0], index=[1]))
            else:
                count2 = count2.append(pd.Series([0, 0], index=[0, 1]))

        count2_json = {
            'failure': count2[0],
            'success': count2[1]
        }
        player_cluster3 = player_defend_data[player_defend_data[shooter_cluster] == 3]
        count3 = player_cluster3.groupby(defend_success)[defend_success].count()
        if count3.shape[0] < 2:
            failure_cluster3 = player_cluster3[player_cluster3[defend_success] == 0]
            success_cluster3 = player_cluster3[player_cluster3[defend_success] == 1]
            if failure_cluster3.shape[0] == 0:
                count3 = count3.append(pd.Series([0], index=[0]))
            elif success_cluster3.shape[0] == 0:
                count3 = count3.append(pd.Series([0], index=[1]))
            else:
                count3 = count3.append(pd.Series([0, 0], index=[1, 0]))

        count3_json = {
            'failure': count3[0],
            'success': count3[1]
        }

        player_cluster4 = player_defend_data[player_defend_data[shooter_cluster] == 4]
        count4 = player_cluster4.groupby(defend_success)[defend_success].count()
        if count4.shape[0] < 2:
            failure_cluster4 = player_cluster4[player_cluster4[defend_success] == 0]
            success_cluster4 = player_cluster4[player_cluster4[defend_success] == 1]
            if failure_cluster4.shape[0] == 0:
                count4 = count4.append(pd.Series([0], index=[0]))
            elif success_cluster4.shape[0] == 0:
                count4 = count4.append(pd.Series([0], index=[1]))
            else:
                count4 = count4.append(pd.Series([0, 0], index=[0, 1]))

        count4_json = {
            'failure': count4[0],
            'success': count4[1]
        }
        data_json = {
            'Cluster 0': count0_json,
            'Cluster 1': count1_json,
            'Cluster 2': count2_json,
            'Cluster 3': count3_json,
            'Cluster 4': count4_json
        }
        if position in ['SG']:
            player_cluster5 = player_defend_data[player_defend_data[shooter_cluster] == 5]
            count5 = player_cluster5.groupby(defend_success)[defend_success].count()
            if count5.shape[0] < 2:
                failure_cluster5 = player_cluster5[player_cluster5[defend_success] == 0]
                success_cluster5 = player_cluster5[player_cluster5[defend_success] == 1]
                if failure_cluster5.shape[0] == 0:
                    count5 = count5.append(pd.Series([0], index=[0]))
                elif success_cluster5.shape[0] == 0:
                    count5 = count5.append(pd.Series([0], index=[0]))
                else:
                    count5 = count5.append(pd.Series([0, 1], index=[0, 1]))
            data_json['Cluster 5'] = {
                'failure': count5[0],
                'success': count5[1]
            }

        return data_json

    @staticmethod
    def get(request, player_id, player_position):
        """

        :param request:
        :param player_id: Player integer identifier to extract defend info
        :param player_position: Player position as string.
        :return:
        """

        defend_data = DatabasemanagerConfig.defend_data
        player_defend_data = defend_data[defend_data['Defender ID'] == player_id]
        player_position = player_position.upper()
        data_json = GetDefendInfo.extract_defend_info(
            player_defend_data[player_defend_data['Shooter position'] == player_position],
            player_position)

        return response.Response(data=data_json, status=status.HTTP_200_OK)


class GetTeamPointsPerPositions(views.APIView):

    @staticmethod
    def get(request, team_id):
        """
        Get the team score distributed by the positions of the players.
        :param request:
        :param team_id: Team integer identifier
        :return:
        """

        points_distribution = {
            'PG': Player.objects.filter(team_id=team_id, position='PG').aggregate(Sum('scored_points'))['scored_points__sum'],
            'SG': Player.objects.filter(team_id=team_id, position='SG').aggregate(Sum('scored_points'))['scored_points__sum'],
            'SF': Player.objects.filter(team_id=team_id, position='SF').aggregate(Sum('scored_points'))['scored_points__sum'],
            'PF': Player.objects.filter(team_id=team_id, position='PF').aggregate(Sum('scored_points'))['scored_points__sum'],
            'C': Player.objects.filter(team_id=team_id, position='C').aggregate(Sum('scored_points'))['scored_points__sum']
        }

        return response.Response(data=points_distribution, status=status.HTTP_200_OK)
