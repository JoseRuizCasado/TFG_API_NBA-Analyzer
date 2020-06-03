from rest_framework import serializers
from .models import Team, Player, Game


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    def create(self, validated_data):
        return Team.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.played_games = validated_data.get('played_games', instance.played_games)
        instance.played_minutes = validated_data.get('played_minutes', instance.played_minutes)
        instance.scored_points = validated_data.get('scored_points', instance.scored_points)
        instance.conceded_points = validated_data.get('conceded_points', instance.conceded_points)
        instance.field_goals_made = validated_data.get('field_goals_made', instance.field_goals_made)
        instance.conceded_field_goals_made = validated_data.get('conceded_field_goals_made',
                                                                instance.conceded_field_goals_made)
        instance.field_goals_attempts = validated_data.get('field_goals_attempts', instance.field_goals_attempts)
        instance.conceded_field_goals_attempts = validated_data.get('conceded_field_goals_attempts',
                                                                    instance.conceded_field_goals_attempts)
        instance.three_points_field_goals_made = validated_data.get('three_points_field_goals_made',
                                                                    instance.three_points_field_goals_made)
        instance.conceded_three_points_field_goals_made = validated_data.get('conceded_three_points_field_goals_made',
                                                                             instance.conceded_three_points_field_goals_made)
        instance.three_points_field_goals_attempts = validated_data.get('three_points_field_goals_attempts',
                                                                        instance.three_points_field_goals_attempts)
        instance.conceded_three_points_field_goals_attempts = validated_data.get(
            'conceded_three_points_field_goals_attempts', instance.conceded_three_points_field_goals_attempts)
        instance.free_throws_made = validated_data.get('free_throws_made', instance.free_throws_made)
        instance.conceded_free_throws_made = validated_data.get('conceded_free_throws_made',
                                                                instance.conceded_free_throws_made)
        instance.free_throws_attempts = validated_data.get('free_throws_attempts', instance.free_throws_attempts)
        instance.conceded_free_throws_attempts = validated_data.get('conceded_free_throws_attempts',
                                                                    instance.conceded_free_throws_attempts)
        instance.assists = validated_data.get('assists', instance.assists)
        instance.conceded_assists = validated_data.get('conceded_assists', instance.conceded_assists)
        instance.offensive_rebounds = validated_data.get('offensive_rebounds', instance.offensive_rebounds)
        instance.conceded_offensive_rebounds = validated_data.get('conceded_offensive_rebounds',
                                                                  instance.conceded_offensive_rebounds)
        instance.defensive_rebounds = validated_data.get('defensive_rebounds', instance.defensive_rebounds)
        instance.conceded_defensive_rebounds = validated_data.get('conceded_defensive_rebounds',
                                                                  instance.conceded_defensive_rebounds)
        instance.steals = validated_data.get('steals', instance.steals)
        instance.conceded_steals = validated_data.get('conceded_steals', instance.conceded_steals)
        instance.blocks = validated_data.get('blocks', instance.blocks)
        instance.conceded_blocks = validated_data.get('conceded_blocks', instance.conceded_blocks)
        instance.turnovers = validated_data.get('turnovers', instance.turnovers)
        instance.conceded_turnovers = validated_data.get('conceded_turnovers', instance.conceded_turnovers)
        instance.personal_fouls = validated_data.get('personal_fouls', instance.personal_fouls)
        instance.conceded_personal_fouls = validated_data.get('conceded_personal_fouls',
                                                              instance.conceded_personal_fouls)
        instance.scored_points_per_game = validated_data.get('scored_points_per_game', instance.scored_points_per_game)
        instance.field_goals_made_per_game = validated_data.get('field_goals_made_per_game',
                                                                instance.field_goals_made_per_game)
        instance.field_goals_attempts_per_game = validated_data.get('field_goals_attempts_per_game',
                                                                    instance.field_goals_attempts_per_game)
        instance.three_points_field_goals_made_per_game = validated_data.get('three_points_field_goals_made_per_game',
                                                                             instance.three_points_field_goals_made_per_game)
        instance.three_points_field_goals_attempts_per_game = validated_data.get(
            'three_points_field_goals_attempts_per_game', instance.three_points_field_goals_attempts_per_game)
        instance.free_throws_made_per_game = validated_data.get('free_throws_made_per_game',
                                                                instance.free_throws_made_per_game)
        instance.free_throws_attempts_per_game = validated_data.get('free_throws_attempts_per_game',
                                                                    instance.free_throws_attempts_per_game)
        instance.assists_per_game = validated_data.get('assists_per_game', instance.assists_per_game)
        instance.offensive_rebounds_per_game = validated_data.get('offensive_rebounds_per_game',
                                                                  instance.offensive_rebounds_per_game)
        instance.defensive_rebounds_per_game = validated_data.get('defensive_rebounds_per_game',
                                                                  instance.defensive_rebounds_per_game)
        instance.steals_per_game = validated_data.get('steals_per_game', instance.steals_per_game)
        instance.blocks_per_game = validated_data.get('blocks_per_game', instance.blocks_per_game)
        instance.turnovers_per_game = validated_data.get('turnovers_per_game', instance.turnovers_per_game)
        instance.personal_fouls_per_game = validated_data.get('personal_fouls_per_game',
                                                              instance.personal_fouls_per_game)

        instance.save()
        return instance


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.team_id = validated_data.get('team_id', instance.team_id)
        instance.played_games = validated_data.get('played_games', instance.played_games)
        instance.played_minutes = validated_data.get('played_minutes', instance.played_minutes)
        instance.scored_points = validated_data.get('scored_points', instance.scored_points)
        instance.field_goals_made = validated_data.get('field_goals_made', instance.field_goals_made)
        instance.field_goals_attempts = validated_data.get('field_goals_attempts', instance.field_goals_attempts)
        instance.three_points_field_goals_made = validated_data.get('three_points_field_goals_made',
                                                                    instance.three_points_field_goals_made)
        instance.three_points_field_goals_attempts = validated_data.get('three_points_field_goals_attempts',
                                                                        instance.three_points_field_goals_attempts)
        instance.free_throws_made = validated_data.get('free_throws_made', instance.free_throws_made)
        instance.free_throws_attempts = validated_data.get('free_throws_attempts', instance.free_throws_attempts)
        instance.assists = validated_data.get('assists', instance.assists)
        instance.offensive_rebounds = validated_data.get('offensive_rebounds', instance.offensive_rebounds)
        instance.defensive_rebounds = validated_data.get('defensive_rebounds', instance.defensive_rebounds)
        instance.steals = validated_data.get('steals', instance.steals)
        instance.blocks = validated_data.get('blocks', instance.blocks)
        instance.turnovers = validated_data.get('turnovers', instance.turnovers)
        instance.personal_fouls = validated_data.get('personal_fouls', instance.personal_fouls)
        instance.scored_points_per_game = validated_data.get('scored_points_per_game', instance.scored_points_per_game)
        instance.field_goals_made_per_game = validated_data.get('field_goals_made_per_game',
                                                                instance.field_goals_made_per_game)
        instance.field_goals_attempts_per_game = validated_data.get('field_goals_attempts_per_game',
                                                                    instance.field_goals_attempts_per_game)
        instance.three_points_field_goals_made_per_game = validated_data.get('three_points_field_goals_made_per_game',
                                                                             instance.three_points_field_goals_made_per_game)
        instance.three_points_field_goals_attempts_per_game = validated_data.get(
            'three_points_field_goals_attempts_per_game', instance.three_points_field_goals_attempts_per_game)
        instance.free_throws_made_per_game = validated_data.get('free_throws_made_per_game',
                                                                instance.free_throws_made_per_game)
        instance.free_throws_attempts_per_game = validated_data.get('free_throws_attempts_per_game',
                                                                    instance.free_throws_attempts_per_game)
        instance.assists_per_game = validated_data.get('assists_per_game', instance.assists_per_game)
        instance.offensive_rebounds_per_game = validated_data.get('offensive_rebounds_per_game',
                                                                  instance.offensive_rebounds_per_game)
        instance.defensive_rebounds_per_game = validated_data.get('defensive_rebounds_per_game',
                                                                  instance.defensive_rebounds_per_game)
        instance.steals_per_game = validated_data.get('steals_per_game', instance.steals_per_game)
        instance.blocks_per_game = validated_data.get('blocks_per_game', instance.blocks_per_game)
        instance.turnovers_per_game = validated_data.get('turnovers_per_game', instance.turnovers_per_game)
        instance.personal_fouls_per_game = validated_data.get('personal_fouls_per_game',
                                                              instance.personal_fouls_per_game)

        instance.save()
        return instance


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data):
        return Game.objects.create(**validated_data)
