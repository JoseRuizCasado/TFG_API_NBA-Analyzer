from rest_framework import serializers
from .models import Team, Player, Game, PlayerShotCharts


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    def create(self, validated_data):
        return Team.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.played_games += validated_data.get('played_games', 0)
        instance.played_minutes += validated_data.get('played_minutes', 0)
        instance.scored_points += validated_data.get('scored_points', 0)
        instance.conceded_points += validated_data.get('conceded_points', 0)
        instance.field_goals_made += validated_data.get('field_goals_made', 0)
        instance.conceded_field_goals_made += validated_data.get('conceded_field_goals_made', 0)

        instance.field_goals_miss += validated_data.get('field_goals_miss', 0)
        instance.conceded_field_goals_miss += validated_data.get('conceded_field_goals_miss', 0)
        instance.field_goals_attempts += validated_data.get('field_goals_attempts', 0)
        instance.conceded_field_goals_attempts += validated_data.get('conceded_field_goals_attempts', 0)
        instance.three_points_field_goals_made += validated_data.get('three_points_field_goals_made', 0)
        instance.conceded_three_points_field_goals_made += \
            validated_data.get('conceded_three_points_field_goals_made', 0)
        instance.three_points_field_goals_miss += validated_data.get('three_points_field_goals_miss', 0)
        instance.conceded_three_points_field_goals_miss += \
            validated_data.get('conceded_three_points_field_goals_miss', 0)
        instance.three_points_field_goals_attempts += validated_data.get('three_points_field_goals_attempts', 0)
        instance.conceded_three_points_field_goals_attempts += \
            validated_data.get('conceded_three_points_field_goals_attempts', 0)
        instance.free_throws_made += validated_data.get('free_throws_made', 0)
        instance.conceded_free_throws_made += validated_data.get('conceded_free_throws_made', 0)
        instance.free_throws_miss += validated_data.get('free_throws_miss', 0)
        instance.conceded_free_throws_miss += validated_data.get('conceded_free_throws_miss', 0)
        instance.free_throws_attempts += validated_data.get('free_throws_attempts', 0)
        instance.conceded_free_throws_attempts += validated_data.get('conceded_free_throws_attempts', 0)
        instance.assists += validated_data.get('assists', 0)
        instance.conceded_assists += validated_data.get('conceded_assists', 0)
        instance.offensive_rebounds += validated_data.get('offensive_rebounds', 0)
        instance.conceded_offensive_rebounds += validated_data.get('conceded_offensive_rebounds', 0)
        instance.defensive_rebounds += validated_data.get('defensive_rebounds', 0)
        instance.conceded_defensive_rebounds += validated_data.get('conceded_defensive_rebounds', 0)
        instance.steals += validated_data.get('steals', 0)
        instance.conceded_steals += validated_data.get('conceded_steals', 0)
        instance.blocks += validated_data.get('blocks', 0)
        instance.conceded_blocks += validated_data.get('conceded_blocks', 0)
        instance.turnovers += validated_data.get('turnovers', 0)
        instance.conceded_turnovers += validated_data.get('conceded_turnovers', 0)
        instance.personal_fouls += validated_data.get('personal_fouls', 0)
        instance.conceded_personal_fouls += validated_data.get('conceded_personal_fouls', 0)
        instance.scored_points_per_game = (validated_data.get('scored_points', 0) + instance.scored_points) \
                                          / (instance.played_games + validated_data.get('played_games', 0))
        instance.field_goals_made_per_game = (validated_data.get('field_goals_made', 0) + instance.field_goals_made) \
                                             / (instance.played_games + validated_data.get('played_games', 0))
        instance.field_goals_miss_per_game = (validated_data.get('field_goals_miss', 0) + instance.field_goals_miss) \
                                             / (instance.played_games + validated_data.get('played_games', 0))
        instance.field_goals_attempts_per_game = \
            (validated_data.get('field_goals_attempts', 0) + instance.field_goals_attempts) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.three_points_field_goals_made_per_game = \
            (validated_data.get('three_points_field_goals_made', 0) + instance.three_points_field_goals_made) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.three_points_field_goals_miss_per_game = \
            (validated_data.get('three_points_field_goals_miss', 0) + instance.three_points_field_goals_miss) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.three_points_field_goals_attempts_per_game = \
            (validated_data.get('three_points_field_goals_attempts', 0) + instance.three_points_field_goals_attempts) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.free_throws_made_per_game = \
            (validated_data.get('free_throws_made', 0) + instance.free_throws_made) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.free_throws_miss_per_game = (validated_data.get('free_throws_miss', 0) + instance.free_throws_miss) \
                                             / (instance.played_games + validated_data.get('played_games', 0))
        instance.free_throws_attempts_per_game = \
            (validated_data.get('free_throws_attempts', 0) + instance.free_throws_attempts) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.assists_per_game = (validated_data.get('assists', 0) + instance.assists) \
                                    / (instance.played_games + validated_data.get('played_games', 0))
        instance.offensive_rebounds_per_game = \
            (validated_data.get('offensive_rebounds', 0) + instance.offensive_rebounds) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.defensive_rebounds_per_game = \
            (validated_data.get('defensive_rebounds', 0) + instance.defensive_rebounds) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.steals_per_game = (validated_data.get('steals', 0) + instance.steals) \
                                   / (instance.played_games + validated_data.get('played_games', 0))
        instance.blocks_per_game = (validated_data.get('blocks', 0) + instance.blocks) \
                                   / (instance.played_games + validated_data.get('played_games', 0))
        instance.turnovers_per_game = (validated_data.get('turnovers', 0) + instance.turnovers) \
                                      / (instance.played_games + validated_data.get('played_games', 0))
        instance.personal_fouls_per_game = (validated_data.get('personal_fouls', 0) + instance.personal_fouls) \
                                           / (instance.played_games + validated_data.get('played_games', 0))

        instance.save()
        return instance


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_starter = validated_data.get('is_starter', instance.is_starter)
        instance.cluster = validated_data.get('cluster', instance.cluster)
        instance.played_games += validated_data.get('played_games', 0)
        instance.played_minutes += validated_data.get('played_minutes', 0)
        instance.scored_points += validated_data.get('scored_points', 0)
        instance.field_goals_made += validated_data.get('field_goals_made', 0)

        instance.field_goals_miss += validated_data.get('field_goals_miss', 0)
        instance.field_goals_attempts += validated_data.get('field_goals_attempts', 0)
        instance.three_points_field_goals_made += validated_data.get('three_points_field_goals_made', 0)
        instance.three_points_field_goals_miss += validated_data.get('three_points_field_goals_miss', 0)
        instance.three_points_field_goals_attempts += validated_data.get('three_points_field_goals_attempts', 0)
        instance.free_throws_made += validated_data.get('free_throws_made', 0)
        instance.free_throws_miss += validated_data.get('free_throws_miss', 0)
        instance.free_throws_attempts += validated_data.get('free_throws_attempts', 0)
        instance.assists += validated_data.get('assists', 0)
        instance.offensive_rebounds += validated_data.get('offensive_rebounds', 0)
        instance.defensive_rebounds += validated_data.get('defensive_rebounds', 0)
        instance.steals += validated_data.get('steals', 0)
        instance.blocks += validated_data.get('blocks', 0)
        instance.turnovers += validated_data.get('turnovers', 0)
        instance.personal_fouls += validated_data.get('personal_fouls', 0)
        instance.played_minutes_per_game = (validated_data.get('played_minutes', 0) + instance.played_minutes) \
                                           / (instance.played_games + validated_data.get('played_games', 0))
        instance.scored_points_per_game = (validated_data.get('scored_points', 0) + instance.scored_points) \
                                          / (instance.played_games + validated_data.get('played_games', 0))
        instance.field_goals_made_per_game = (validated_data.get('field_goals_made', 0) + instance.field_goals_made) \
                                             / (instance.played_games + validated_data.get('played_games', 0))
        instance.field_goals_miss_per_game = (validated_data.get('field_goals_miss', 0) + instance.field_goals_miss) \
                                             / (instance.played_games + validated_data.get('played_games', 0))
        instance.field_goals_attempts_per_game = \
            (validated_data.get('field_goals_attempts', 0) + instance.field_goals_attempts) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.three_points_field_goals_made_per_game = \
            (validated_data.get('three_points_field_goals_made', 0) + instance.three_points_field_goals_made) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.three_points_field_goals_miss_per_game = \
            (validated_data.get('three_points_field_goals_miss', 0) + instance.three_points_field_goals_miss) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.three_points_field_goals_attempts_per_game = \
            (validated_data.get('three_points_field_goals_attempts', 0) + instance.three_points_field_goals_attempts) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.free_throws_made_per_game = \
            (validated_data.get('free_throws_made', 0) + instance.free_throws_made) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.free_throws_miss_per_game = (validated_data.get('free_throws_miss', 0) + instance.free_throws_miss) \
                                             / (instance.played_games + validated_data.get('played_games', 0))
        instance.free_throws_attempts_per_game = \
            (validated_data.get('free_throws_attempts', 0) + instance.free_throws_attempts) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.assists_per_game = (validated_data.get('assists', 0) + instance.assists) \
                                    / (instance.played_games + validated_data.get('played_games', 0))
        instance.offensive_rebounds_per_game = \
            (validated_data.get('offensive_rebounds', 0) + instance.offensive_rebounds) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.defensive_rebounds_per_game = \
            (validated_data.get('defensive_rebounds', 0) + instance.defensive_rebounds) \
            / (instance.played_games + validated_data.get('played_games', 0))
        instance.steals_per_game = (validated_data.get('steals', 0) + instance.steals) \
                                   / (instance.played_games + validated_data.get('played_games', 0))
        instance.blocks_per_game = (validated_data.get('blocks', 0) + instance.blocks) \
                                   / (instance.played_games + validated_data.get('played_games', 0))
        instance.turnovers_per_game = (validated_data.get('turnovers', 0) + instance.turnovers) \
                                      / (instance.played_games + validated_data.get('played_games', 0))
        instance.personal_fouls_per_game = (validated_data.get('personal_fouls', 0) + instance.personal_fouls) \
                                           / (instance.played_games + validated_data.get('played_games', 0))

        instance.save()
        return instance


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.information_loaded = validated_data.get('information_loaded', instance.information_loaded)
        instance.save()
        return instance


class PlayerShotChartSerializer(serializers.ModelSerializer):
    scatter_chart = serializers.ImageField(max_length=None, use_url=True)
    hexbin_chart = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = PlayerShotCharts
        fields = '__all__'

    def create(self, validated_data):
        return PlayerShotCharts.objects.create(**validated_data)
