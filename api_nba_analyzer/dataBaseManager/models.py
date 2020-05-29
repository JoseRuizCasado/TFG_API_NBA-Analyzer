from django.db import models


# Create your models here.

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=255, null=False)
    abbreviation = models.CharField(max_length=255, null=False)

    class Conference(models.TextChoices):
        WESTERN = 'WESTERN'
        EASTERN = 'EASTERN'

    conference = models.CharField(max_length=255, null=False, choices=Conference.choices)

    class Division(models.TextChoices):
        ATLANTIC = 'ATLANTIC'
        CENTRAL = 'CENTRAL'
        SOUTHEAST = 'SOUTHWEST'
        NORTHWEST = 'NORTHWEST'
        PACIFIC = 'PACIFIC'
        SOUTHWEST = 'SOUTHWEST'

    division = models.CharField(max_length=255, null=True, choices=Division.choices)
    city = models.CharField(max_length=255, null=True)
    head_coach_name = models.CharField(max_length=255, null=True)
    general_manager_name = models.CharField(max_length=255, null=True)
    played_games = models.IntegerField(null=False, default=0)
    scored_points = models.IntegerField(null=False, default=0)
    conceded_points = models.IntegerField(null=False, default=0)
    field_goals_made = models.IntegerField(null=False, default=0)
    conceded_field_goals_made = models.IntegerField(null=False, default=0)
    field_goals_attempts = models.IntegerField(null=False, default=0)
    conceded_field_goals_attempts = models.IntegerField(null=False, default=0)
    three_points_field_goals_made = models.IntegerField(null=False, default=0)
    conceded_three_points_field_goals_made = models.IntegerField(null=False, default=0)
    three_points_field_goals_attempts = models.IntegerField(null=False, default=0)
    conceded_three_points_field_goals_attempts = models.IntegerField(null=False, default=0)
    free_throws_made = models.IntegerField(null=False, default=0)
    conceded_free_throws_made = models.IntegerField(null=False, default=0)
    assists = models.IntegerField(null=False, default=0)
    conceded_assists = models.IntegerField(null=False, default=0)
    offensive_rebounds = models.IntegerField(null=False, default=0)
    conceded_offensive_rebounds = models.IntegerField(null=False, default=0)
    defensive_rebounds = models.IntegerField(null=False, default=0)
    conceded_defensive_rebounds = models.IntegerField(null=False, default=0)
    steals = models.IntegerField(null=False, default=0)
    conceded_steals = models.IntegerField(null=False, default=0)
    blocks = models.IntegerField(null=False, default=0)
    conceded_blocks = models.IntegerField(null=False, default=0)
    turnovers = models.IntegerField(null=False, default=0)
    conceded_turnovers = models.IntegerField(null=False, default=0)
    personal_fouls = models.IntegerField(null=False, default=0)
    conceded_personal_fouls = models.IntegerField(null=False, default=0)
    scored_points_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    field_goals_made_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    field_goals_attempts_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    three_points_field_goals_made_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    three_points_field_goals_attempts_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    free_throws_made_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    free_throws_attempts_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    assists_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    offensive_rebounds_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    defensive_rebounds_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    steals_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    blocks_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    turnovers_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)
    personal_fouls_per_game = models.DecimalField(null=False, default=0.00, decimal_places=3)

