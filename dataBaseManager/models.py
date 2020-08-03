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
        SOUTHEAST = 'SOUTHEAST'
        NORTHWEST = 'NORTHWEST'
        PACIFIC = 'PACIFIC'
        SOUTHWEST = 'SOUTHWEST'

    division = models.CharField(max_length=255, null=True, choices=Division.choices)
    city = models.CharField(max_length=255, null=True)
    head_coach_name = models.CharField(max_length=255, null=True)
    general_manager_name = models.CharField(max_length=255, null=True)
    played_games = models.IntegerField(null=False, default=0)
    played_minutes = models.IntegerField(null=False, default=0)
    scored_points = models.IntegerField(null=False, default=0)
    conceded_points = models.IntegerField(null=False, default=0)
    field_goals_made = models.IntegerField(null=False, default=0)
    conceded_field_goals_made = models.IntegerField(null=False, default=0)
    field_goals_miss = models.IntegerField(null=False, default=0)
    conceded_field_goals_miss = models.IntegerField(null=False, default=0)
    field_goals_attempts = models.IntegerField(null=False, default=0)
    conceded_field_goals_attempts = models.IntegerField(null=False, default=0)
    three_points_field_goals_made = models.IntegerField(null=False, default=0)
    conceded_three_points_field_goals_made = models.IntegerField(null=False, default=0)
    three_points_field_goals_miss = models.IntegerField(null=False, default=0)
    conceded_three_points_field_goals_miss = models.IntegerField(null=False, default=0)
    three_points_field_goals_attempts = models.IntegerField(null=False, default=0)
    conceded_three_points_field_goals_attempts = models.IntegerField(null=False, default=0)
    free_throws_made = models.IntegerField(null=False, default=0)
    conceded_free_throws_made = models.IntegerField(null=False, default=0)
    free_throws_miss = models.IntegerField(null=False, default=0)
    conceded_free_throws_miss = models.IntegerField(null=False, default=0)
    free_throws_attempts = models.IntegerField(null=False, default=0)
    conceded_free_throws_attempts = models.IntegerField(null=False, default=0)
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
    scored_points_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    field_goals_made_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    field_goals_miss_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    field_goals_attempts_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    three_points_field_goals_made_per_game = models.DecimalField(null=False, default=0.00, max_digits=65,
                                                                 decimal_places=3)
    three_points_field_goals_attempts_per_game = models.DecimalField(null=False, max_digits=65, default=0.00,
                                                                     decimal_places=3)
    free_throws_made_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    free_throws_miss_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    free_throws_attempts_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    assists_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    offensive_rebounds_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    defensive_rebounds_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    steals_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    blocks_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    turnovers_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    personal_fouls_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['name']

    def __str__(self):
        return self.name


class Player(models.Model):
    player_id = models.IntegerField(primary_key=True, null=False)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    jersey = models.IntegerField(null=False)
    birth_date = models.DateField(null=False)
    height = models.IntegerField(null=False)
    weight = models.IntegerField(null=False)

    class Position(models.TextChoices):
        POINTGUARD = 'PG'
        SHOOTINGGUARD = 'SG'
        SMALLFORWARD = 'SF'
        POWERFORWARD = 'PF'
        CENTER = 'C'

    position = models.CharField(null=False, max_length=255, choices=Position.choices)
    played_games = models.IntegerField(null=False, default=0)
    played_minutes = models.IntegerField(null=False, default=0)
    scored_points = models.IntegerField(null=False, default=0)
    field_goals_made = models.IntegerField(null=False, default=0)
    field_goals_miss = models.IntegerField(null=False, default=0)
    field_goals_attempts = models.IntegerField(null=False, default=0)
    three_points_field_goals_made = models.IntegerField(null=False, default=0)
    three_points_field_goals_miss = models.IntegerField(null=False, default=0)
    three_points_field_goals_attempts = models.IntegerField(null=False, default=0)
    free_throws_made = models.IntegerField(null=False, default=0)
    free_throws_miss = models.IntegerField(null=False, default=0)
    free_throws_attempts = models.IntegerField(null=False, default=0)
    assists = models.IntegerField(null=False, default=0)
    offensive_rebounds = models.IntegerField(null=False, default=0)
    defensive_rebounds = models.IntegerField(null=False, default=0)
    steals = models.IntegerField(null=False, default=0)
    blocks = models.IntegerField(null=False, default=0)
    turnovers = models.IntegerField(null=False, default=0)
    personal_fouls = models.IntegerField(null=False, default=0)
    played_minutes_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    scored_points_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    field_goals_made_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    field_goals_miss_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    field_goals_attempts_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    three_points_field_goals_made_per_game = models.DecimalField(null=False, default=0.00, max_digits=65,
                                                                 decimal_places=3)
    three_points_field_goals_attempts_per_game = models.DecimalField(null=False, default=0.00, max_digits=65,
                                                                     decimal_places=3)
    free_throws_made_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    free_throws_miss_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    free_throws_attempts_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    assists_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    offensive_rebounds_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    defensive_rebounds_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    steals_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    blocks_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    turnovers_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)
    personal_fouls_per_game = models.DecimalField(null=False, default=0.00, max_digits=65, decimal_places=3)

    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        ordering = ['team_id']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Game(models.Model):
    game_id = models.CharField(max_length=255, primary_key=True, null=False)
    information_loaded = models.BooleanField(null=False, default=False)
    local_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='local_team')
    visitor_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='visitor_team')
    winner_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner_team')

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        ordering = ['game_id']

    def __str__(self):
        return f'{self.visitor_team} VS@ {self.local_team}'


class DefendInfo(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    shooter_id = models.IntegerField(null=False)
    defender_id = models.IntegerField(null=False)
    defend_success = models.BooleanField(null=False)

    def __str__(self):
        if self.defend_success:
            return f'{self.shooter_id} miss shot defended by {self.defender_id}'
        else:
            return f'{self.shooter_id} made shot defended by {self.defender_id}'
