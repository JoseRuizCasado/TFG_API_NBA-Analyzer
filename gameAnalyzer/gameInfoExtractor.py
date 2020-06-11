import re

import pandas as pd


def extract_game_info(game_id, team_id, players, description):
    """
    Extract info from game files
    :param game_id: string game id to load game files
    :param team_id:
    :param players:
    :param description:
    :return:
    """
    players_list = []
    # Create dict to save Player info
    for player in players:
        player_dict = {
            'player_id': player['player_id'],
            'played_games': 0,
            'played_minutes': 0,
            'scored_points': 0,
            'field_goals_made': 0,
            'field_goals_miss': 0,
            'field_goals_attempts': 0,
            'three_points_field_goals_made': 0,
            'three_points_field_goals_miss': 0,
            'three_points_field_goals_attempts': 0,
            'free_throws_made': 0,
            'free_throws_miss': 0,
            'free_throws_attempts': 0,
            'assists': 0,
            'offensive_rebounds': 0,
            'defensive_rebounds': 0,
            'steals': 0,
            'blocks': 0,
            'turnovers': 0,
            'personal_fouls': 0
        }
        players_list.append(player_dict)

    # Create dict to save Team info
    team_dict = {
        'team_id': team_id,
        'played_games': 1,
        'played_minutes': 2880,  # Add whole game time to Team played minutes
        'scored_points': 0,
        'field_goals_made': 0,
        'field_goals_miss': 0,
        'field_goals_attempts': 0,
        'three_points_field_goals_made': 0,
        'three_points_field_goals_miss': 0,
        'three_points_field_goals_attempts': 0,
        'free_throws_made': 0,
        'free_throws_miss': 0,
        'free_throws_attempts': 0,
        'assists': 0,
        'offensive_rebounds': 0,
        'defensive_rebounds': 0,
        'steals': 0,
        'blocks': 0,
        'turnovers': 0,
        'personal_fouls': 0,
        'players': players_list
    }

    # Reading play-by-play Game file
    game_data = pd.read_csv(f'../data/events/{game_id}.csv')

    # Load Game events
    made_shots = game_data[game_data['EVENTMSGTYPE'] == 1]
    missed_shots = game_data[game_data['EVENTMSGTYPE'] == 2]
    free_throws = game_data[game_data['EVENTMSGTYPE'] == 3]
    rebounds = game_data[game_data['EVENTMSGTYPE'] == 4]
    turnovers = game_data[game_data['EVENTMSGTYPE'] == 5]
    personal_fouls = game_data[game_data['EVENTMSGTYPE'] == 6]
    substitutions = game_data[game_data['EVENTMSGTYPE'] == 8]

    # Read Team data, player by player
    for player in team_dict['players']:
        # Load Player made shots
        player_shots = made_shots[made_shots['PLAYER1_ID'] == player['player_id']]
        # Load Player field goals made
        player_field_goals = player_shots.shape[0]
        # Load Player 3 field goals made
        player_3pt = player_shots[player_shots['HOMEDESCRIPTION'].str.contains('3PT')].shape[0]
        # Load Player assists
        player_assists = made_shots[made_shots['PLAYER2_ID'] == player['player_id']].shape[0]
        # TODO: Load shots coordinates

        # Load Player missed shots
        player_misses = missed_shots[missed_shots['PLAYER1_ID'] == player['player_id']]
        # Load Player field goals misses.
        player_field_goals_misses = player_misses.shape[0]
        # Load Player 3 field goals made.
        player_3pt_misses = player_misses[player_misses[description].str.contains('3PT')].shape[0]

        # Load Player made free throws.
        player_free_throw = free_throws[free_throws['PLAYER1_ID'] == player['player_id']]
        # Load Player missed free throws.
        player_free_throw_misses = player_free_throw[player_free_throw[description].str.contains('MISS')].shape[0]
        # Load PLayer made free throws.
        player_free_throw_made = player_free_throw[~player_free_throw[description].str.contains('MISS')].shape[0]
        # Load Player blocks.
        player_blocks = missed_shots[missed_shots['PLAYER3_ID'] == player['player_id']].shape[0]

        # Load Player rebounds
        player_rebounds = rebounds[rebounds['PLAYER1_ID'] == player['player_id']]
        # We need to extract rebound from description (Off:x Def:y).
        last_rebound_row = player_rebounds.tail(1)
        string_rebounds = str(last_rebound_row[description].max())
        if string_rebounds != 'nan':
            # Extract offensive rebounds.
            pattern = re.compile('Off:[0-9]*')
            offensive_rebounds = pattern.search(string_rebounds).group(0)
            offensive_rebounds = int(re.sub('Off:', '', offensive_rebounds))
            # Extract defensive rebounds
            pattern = re.compile('Def:[0-9]*')
            defensive_rebounds = pattern.search(string_rebounds).group(0)
            defensive_rebounds = int(re.sub('Def:', '', defensive_rebounds))
        else:
            offensive_rebounds = 0
            defensive_rebounds = 0

        # Load Player turnovers
        player_turnovers = turnovers[turnovers['PLAYER1_ID'] == player['player_id']].shape[0]
        # Load Player steals.
        player_steals = turnovers[turnovers['PLAYER2_ID'] == player['player_id']].shape[0]

        # Load Player personal fouls.
        player_personal_fouls = personal_fouls[personal_fouls['PLAYER1_ID'] == player['player_id']]
        player_personal_fouls = player_personal_fouls[~player_personal_fouls['HOMEDESCRIPTION']
            .str.contains('L.B.FOUL')].shape[0]

        # Calculate Player minutes played
        player_substitutions = substitutions[(substitutions['PLAYER1_ID'] == player['player_id'])
                                             | (substitutions['PLAYER2_ID'] == player['player_id'])]
        minutes_played = 0
        last_quarter = 0
        for index, row in player_substitutions.iterrows():
            if row['PLAYER1_ID'] == player['player_id']:
                # Player leaves the game
                minutes = int(re.sub(':[0-9]*', '', row['PCTIMESTRING']))
                seconds = int(re.sub('[0-9]*:', '', row['PCTIMESTRING']))
                if last_quarter != row['PERIOD']:
                    # Doesn't exist IN event associated to this OUT event
                    minutes_played += 720 - (60 * minutes + seconds)

                else:
                    # Exist IN event associated to this OUT event
                    minutes_played -= (minutes * 60 + seconds)

                last_quarter = row['PERIOD']

            elif row['PLAYER2_ID'] == player['player_id']:
                # Player enters the game
                minutes = int(re.sub(':[0-9]*', '', row['PCTIMESTRING']))
                seconds = int(re.sub('[0-9]*:', '', row['PCTIMESTRING']))
                minutes_played += minutes * 60 + seconds

                if row['PERIOD'] > last_quarter + 1:
                    # We haven't Player substitution data from last quarter
                    # We check if the player has record some event,
                    # if he record some event, we assume that he plays all the quarter
                    quarter_data = game_data[game_data['PERIOD'] == last_quarter + 1]
                    quarter_data = quarter_data[(quarter_data['PLAYER1_ID'] == player['player_id'])
                                                | (quarter_data['PLAYER2_ID'] == player['player_id'])
                                                | (quarter_data['PLAYER3_ID'] == player['player_id'])]
                    if quarter_data.shape[0] > 0:
                        minutes_played += 720

                last_quarter = row['PERIOD']

                player['scored_points'] = (player_field_goals - player_3pt) * 2 + player_3pt * 3
                player['minutes_played'] = minutes_played
                player['field_goals_made'] = player_field_goals
                player['field_goals_miss'] = player_field_goals_misses
                player['field_goals_attempts'] = player_field_goals + player_field_goals_misses
                player['three_points_field_goals_made'] = player_3pt
                player['three_points_field_goals_miss'] = player_3pt_misses
                player['three_points_field_goals_attempts'] = player_3pt + player_3pt_misses
                player['free_throws_made'] = player_free_throw_made
                player['free_throws_miss'] = player_free_throw_misses
                player['free_throws_attempts'] = player_free_throw_made + player_free_throw_misses
                player['assists'] = player_assists
                player['offensive_rebounds'] = offensive_rebounds
                player['defensive_rebounds'] = defensive_rebounds
                player['steals'] = player_steals
                player['blocks'] = player_blocks
                player['turnovers'] = player_turnovers
                player['personal_fouls'] = player_personal_fouls

                team_dict['scored_points'] += player['scored_points']
                team_dict['field_goals_made'] += player['field_goals_made']
                team_dict['field_goals_miss'] += player['field_goals_miss']
                team_dict['field_goals_attempts'] += player['field_goals_attempts']
                team_dict['three_points_field_goals_made'] += player['three_points_field_goals_made']
                team_dict['three_points_field_goals_miss'] += player['three_points_field_goals_miss']
                team_dict['three_points_field_goals_attempts'] += player['three_points_field_goals_attempts']
                team_dict['free_throws_made'] += player['free_throws_made']
                team_dict['free_throws_miss'] += player['free_throws_miss']
                team_dict['free_throws_attempts'] += player['free_throws_attempts']
                team_dict['assists'] += player['assists']
                team_dict['offensive_rebounds'] += player['offensive_rebounds']
                team_dict['defensive_rebounds'] += player['defensive_rebounds']
                team_dict['steals'] += player['steals']
                team_dict['blocks'] += player['blocks']
                team_dict['turnovers'] += player['turnovers']
                team_dict['personal_fouls'] += player['personal_fouls']