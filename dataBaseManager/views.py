from operator import itemgetter

from django.core.files import File
from django.db.models import Q, Sum
from rest_framework import views, response, status
from .models import Team, Player, Game, PlayerShotCharts
from .serializer import TeamSerializer, PlayerSerializer, GameSerializer, PlayerShotChartSerializer
import pandas as pd
from .apps import DatabasemanagerConfig
from .ShotMaker import make_hexbin_plot, make_scatter_plot


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
            'Cluster 4': count4_json,
            'Cluster 5': {
                'failure': 0,
                'success': 0
            }
        }
        if position in ['SG', 'PF']:
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
    def extract_cluster_mean_defend_data(defend_data, position, cluster):
        shooter_cluster = 'Shooter Cluster'
        defender_cluster = 'Defender Cluster'
        defend_success = 'Defend Success'
        cluster_mean_json = {
            'Cluster 0': {},
            'Cluster 1': {},
            'Cluster 2': {},
            'Cluster 3': {},
            'Cluster 4': {},
            'Cluster 5': {
                'failure': 0,
                'success': 0
            }
        }

        if cluster != -1:
            cluster_defend_data = defend_data[defend_data[defender_cluster] == cluster]
            cluster0_data = cluster_defend_data[cluster_defend_data[shooter_cluster] == 0]
            cluster_mean_json['Cluster 0'] = {
                'failure': cluster0_data[cluster0_data[defend_success] == 0].shape[0],
                'success': cluster0_data[cluster0_data[defend_success] == 1].shape[0]
            }
            cluster1_data = cluster_defend_data[cluster_defend_data[shooter_cluster] == 1]
            cluster_mean_json['Cluster 1'] = {
                'failure': cluster1_data[cluster1_data[defend_success] == 0].shape[0],
                'success': cluster1_data[cluster1_data[defend_success] == 1].shape[0]
            }
            cluster2_data = cluster_defend_data[cluster_defend_data[shooter_cluster] == 2]
            cluster_mean_json['Cluster 2'] = {
                'failure': cluster2_data[cluster2_data[defend_success] == 0].shape[0],
                'success': cluster2_data[cluster2_data[defend_success] == 1].shape[0]
            }
            cluster3_data = cluster_defend_data[cluster_defend_data[shooter_cluster] == 3]
            cluster_mean_json['Cluster 3'] = {
                'failure': cluster3_data[cluster3_data[defend_success] == 0].shape[0],
                'success': cluster3_data[cluster3_data[defend_success] == 1].shape[0]
            }
            cluster4_data = cluster_defend_data[cluster_defend_data[shooter_cluster] == 4]
            cluster_mean_json['Cluster 4'] = {
                'failure': cluster4_data[cluster4_data[defend_success] == 0].shape[0],
                'success': cluster4_data[cluster4_data[defend_success] == 1].shape[0]
            }

            if position in ['SG']:
                cluster5_data = cluster_defend_data[cluster_defend_data[shooter_cluster] == 5]
                cluster_mean_json['Cluster 5'] = {
                    'failure': cluster5_data[cluster5_data[defend_success] == 0].shape[0],
                    'success': cluster5_data[cluster5_data[defend_success] == 1].shape[0]
                }

        return cluster_mean_json

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
        cluster_data = GetDefendInfo.extract_cluster_mean_defend_data(
            defend_data[(defend_data['Shooter position'] == player_position)], player_position,
            Player.objects.get(player_id=player_id).cluster)

        return response.Response(data={'player_data': data_json, 'cluster_data': cluster_data},
                                 status=status.HTTP_200_OK)


class GetBetterDefenderByOpponentStarters(views.APIView):

    @staticmethod
    def get_defend_accuracy(shooter_cluster, position, player_id):
        shooter_cluster_col = 'Shooter Cluster'
        defend_success = 'Defend Success'
        defend_data = DatabasemanagerConfig.defend_data
        player_defend_data = defend_data[(defend_data['Defender ID'] == player_id)
                                         & (defend_data[shooter_cluster_col] == shooter_cluster)
                                         & (defend_data['Defender position'] == position.upper())
                                         & (defend_data['Shooter position'] == position.upper())]

        total = player_defend_data.shape[0]
        if total > 0:
            success = player_defend_data[player_defend_data[defend_success] == 1].shape[0]
            return success / total
        else:
            return 0

    @staticmethod
    def get(request, team_id, opponent_team_id):
        """
        Get the best starting line up base on the starting line up of the opponent team.
        :param request:
        :param team_id: Team numerical identifier
        :param opponent_team_id: Opponent Team numerical identifier
        :return: JSON with better option per position:
            {
                "PG": "D'Angelo Russel",
                "OpPG": "Jeff Teague",
                "SG": "Kobe Bryant",
                "OpSG": "Kyle Korver",
                "SF": "Anthony Brown",
                "OpSF": "Kent Bazemore",
                "PF": "Julius Randle",
                "OpPF": "Paul Millsap",
                "C": "Roy Hibbert",
                "OpC": "Al Horford"
            }
        """
        best_defenders = []
        opponents_starters = []
        for starter in Player.objects.filter(team_id=opponent_team_id, is_starter=True).order_by('position'):
            print(f'name: {starter.first_name} {starter.last_name}, position: {starter.position}')
            opponents_starters.append(starter.player_id)
            accuracy = []
            for player in Player.objects.filter(team_id=team_id, position=starter.position):
                accuracy.append((player.player_id,
                                 GetBetterDefenderByOpponentStarters.get_defend_accuracy(player.cluster,
                                                                                         starter.position,
                                                                                         player.player_id)))

            best_option = max(accuracy, key=itemgetter(1))[0]
            if best_option in best_defenders:
                res = [it for it in accuracy if it[0] != best_option]
                best_option = max(res, key=itemgetter(1))[0]

            best_defenders.append(best_option)

        pg_player = Player.objects.get(player_id=best_defenders[2])
        opponent_pg_player = Player.objects.get(player_id=opponents_starters[2])
        sg_player = Player.objects.get(player_id=best_defenders[4])
        opponent_sg_player = Player.objects.get(player_id=opponents_starters[4])
        sf_player = Player.objects.get(player_id=best_defenders[3])
        opponent_sf_player = Player.objects.get(player_id=opponents_starters[3])
        pf_player = Player.objects.get(player_id=best_defenders[1])
        opponent_pf_player = Player.objects.get(player_id=opponents_starters[1])
        c_player = Player.objects.get(player_id=best_defenders[0])
        opponent_c_player = Player.objects.get(player_id=opponents_starters[0])

        best_defenders = {
            'PG': f'{pg_player.first_name} {pg_player.last_name}',
            'OpPG': f'{opponent_pg_player.first_name} {opponent_pg_player.last_name}',
            'SG': f'{sg_player.first_name} {sg_player.last_name}',
            'OpSG': f'{opponent_sg_player.first_name} {opponent_sg_player.last_name}',
            'SF': f'{sf_player.first_name} {sf_player.last_name}',
            'OpSF': f'{opponent_sf_player.first_name} {opponent_sf_player.last_name}',
            'PF': f'{pf_player.first_name} {pf_player.last_name}',
            'OpPF': f'{opponent_pf_player.first_name} {opponent_pf_player.last_name}',
            'C': f'{c_player.first_name} {c_player.last_name}',
            'OpC': f'{opponent_c_player.first_name} {opponent_c_player.last_name}'
        }

        return response.Response(data=best_defenders, status=status.HTTP_200_OK)


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
            'PG': Player.objects.filter(team_id=team_id, position='PG').aggregate(Sum('scored_points'))[
                'scored_points__sum'],
            'SG': Player.objects.filter(team_id=team_id, position='SG').aggregate(Sum('scored_points'))[
                'scored_points__sum'],
            'SF': Player.objects.filter(team_id=team_id, position='SF').aggregate(Sum('scored_points'))[
                'scored_points__sum'],
            'PF': Player.objects.filter(team_id=team_id, position='PF').aggregate(Sum('scored_points'))[
                'scored_points__sum'],
            'C': Player.objects.filter(team_id=team_id, position='C').aggregate(Sum('scored_points'))[
                'scored_points__sum']
        }

        starters = Player.objects.filter(team_id=team_id, is_starter=True)

        starters_json = {}
        pg = False
        sg = False
        sf = False
        pf = False
        c = False
        for player in starters:
            if player.position == 'PG':
                if not pg:
                    pg = True
                    starters_json['PG_Starter'] = player.scored_points
                    starters_json['PG_Subs'] = abs(points_distribution['PG'] - player.scored_points)

                else:
                    starters_json['SG_Starter'] = player.scored_points
                    starters_json['SG_Subs'] = abs(points_distribution['SG'] - player.scored_points)

            if player.position == 'SG':
                if not sg:
                    sg = True
                    starters_json['SG_Starter'] = player.scored_points
                    starters_json['SG_Subs'] = abs(points_distribution['SG'] - player.scored_points)

                else:
                    starters_json['SF_Starter'] = player.scored_points
                    starters_json['SF_Subs'] = abs(points_distribution['SF'] - player.scored_points)

            if player.position == 'SF':
                if not sf:
                    sf = True
                    starters_json['SF_Starter'] = player.scored_points
                    starters_json['SF_Subs'] = abs(points_distribution['SF'] - player.scored_points)

                else:
                    starters_json['PF_Starter'] = player.scored_points
                    starters_json['PF_Subs'] = abs(points_distribution['PF'] - player.scored_points)

            if player.position == 'PF':
                if not pf:
                    pf = True
                    starters_json['PF_Starter'] = player.scored_points
                    starters_json['PF_Subs'] = abs(points_distribution['PF'] - player.scored_points)

                else:
                    starters_json['C_Starter'] = player.scored_points
                    starters_json['C_Subs'] = abs(points_distribution['C'] - player.scored_points)

            if player.position == 'C':
                if not c:
                    c = True
                    starters_json['C_Starter'] = player.scored_points
                    starters_json['C_Subs'] = abs(points_distribution['C'] - player.scored_points)

                else:
                    starters_json['PF_Starter'] = player.scored_points
                    starters_json['PF_Subs'] = abs(points_distribution['PF'] - player.scored_points)

        return response.Response(data={'points_distribution': points_distribution,
                                       'starters_sub_distribution': starters_json}, status=status.HTTP_200_OK)


class GetShotChart(views.APIView):

    @staticmethod
    def get(request, image_pk):
        """

        :param request:
        :param image_pk: Player id to take his shots charts.
        :return: shot charts url.
        """
        chart = PlayerShotCharts.objects.get(chart_pk=image_pk)
        serializer = PlayerShotChartSerializer(chart)
        return response.Response(data={'data': serializer.data}, status=status.HTTP_200_OK)


class PostShotCharts(views.APIView):

    @staticmethod
    def post(request, player_id):
        """

        :param request:
        :param player_id: Player id to make his shots charts
        :return:
        """
        shot_data = DatabasemanagerConfig.shot_data
        scatter_path = make_scatter_plot(shot_data[shot_data['PLAYER_ID'] == player_id], player_id)
        hexbin_path = make_hexbin_plot(shot_data[shot_data['PLAYER_ID'] == player_id], player_id)

        player_shot_charts = PlayerShotCharts()
        player_shot_charts.chart_pk = player_id
        player_shot_charts.scatter_chart.save(scatter_path, File(open(scatter_path, 'rb')))
        player_shot_charts.hexbin_chart.save(hexbin_path, File(open(hexbin_path, 'rb')))
        player_shot_charts.save()

        return response.Response(status=status.HTTP_200_OK)
