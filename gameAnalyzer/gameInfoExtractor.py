import math
import re
import pandas as pd
import json
from DefendDataFileManager import insert_defend_data


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def guess_defender(shots_events, misses, game_id):
    with open(f'gameAnalyzer/data/tracking/{game_id}') as json_file:
        coordinates = json.load(json_file)

    shooter_defender_list = []
    for ind, shot in shots_events.iterrows():
        print(f'Event: {shot["EVENTNUM"]}, game {game_id}')
        event = [e for e in coordinates['events'] if int(e['eventId']) == shot['EVENTNUM']]
        event_defenders = []
        cont = -1
        if event:
            for moment in event[0]['moments']:
                cont += 1
                print(cont)
                # Take shooter coordinates
                player_coordinates_moment_list = [p for p in moment[5] if int(p[1]) == shot['PLAYER1_ID']]
                print(f'Moment list: {player_coordinates_moment_list}, player id: {shot["PLAYER1_ID"]}')
                if player_coordinates_moment_list:
                    player_coordinates_moment = player_coordinates_moment_list[0]
                    player_x, player_y = (player_coordinates_moment[2], player_coordinates_moment[3])
                    # Take the players from the opposite team to the shooter.
                    possible_defenders = [d for d in moment[5] if
                                          (int(d[0]) != shot['PLAYER1_TEAM_ID']) & (int(d[0]) != -1)]
                    if possible_defenders:
                        # Compute the distance of each possible defender to the shooter.
                        defenders_distance = [distance(player_x, player_y, defender[2], defender[3]) for defender in
                                              possible_defenders]
                        # Select the lowest distance.
                        min_distance = min(defenders_distance)
                        # Get the nearest defender.
                        nearest_defender = [d for d in possible_defenders if
                                            distance(player_x, player_y, d[2], d[3]) == min_distance]
                        event_defenders.append(nearest_defender[0][1])

        # The selected defender will be the defender that has more appearances as defender through all moment recorded
        # for the shoot event.
        # Calculate the appearances of each defender in the list.
        print(f'Possible defenders: {event_defenders}')
        defender_appearances = [event_defenders.count(d) for d in event_defenders]
        if defender_appearances:
            # Take the maximum appearances
            max_appearances = max(defender_appearances)
            # Transform defender list to avoid duplicates items.
            defenders_list = list(dict.fromkeys(event_defenders))
            # Take the defenders who have more appearances in the list.
            defender = [d for d in defenders_list if event_defenders.count(d) == max_appearances]
            shooter_defender_list.append((shot['PLAYER1_ID'], defender[0], misses))

    return shooter_defender_list


def extract_player_shots_coordinates(game_id, player_id, team_id):
    """
    Extract shot coordinates for each recorder shot of the player in the game.
    Then save extracted coordinates in the player associated json file.
    :param game_id: Game string identifies, matches the files' name.
    :param player_id: Player num that identifies the player.
    :param team_id: Team num that identifies the player team.
    :return:
    """
    # print(f'Extracting coordinates of: {player_id}')
    shots_data = pd.read_csv('gameAnalyzer/data/shots/shots.csv')
    player_json = {
        'made_shots': [],
        'miss_shots': []
    }

    shots_data = shots_data[(shots_data['GAME_ID'] == int(game_id)) & (shots_data['PLAYER_ID'] == player_id)]
    for index, shot in shots_data.iterrows():
        x = shot['LOC_X']
        y = shot['LOC_Y']
        if shot['SHOT_MADE_FLAG']:
            # Made shot
            player_json['made_shots'].append({'x': x, 'y': y})
        else:
            # Miss shot
            player_json['miss_shots'].append({'x': x, 'y': y})

    try:
        with open(f'gameAnalyzer/data/coordinates/{team_id}/{player_id}.json', 'r') as json_data:
            player_coordinates_data = json.load(json_data)
            player_json['made_shots'].extend(player_coordinates_data['made_shots'])
            player_json['miss_shots'].extend(player_coordinates_data['miss_shots'])
    except Exception:
        print(f'Does not exist file associated to the player {player_id}')

    with open(f'gameAnalyzer/data/coordinates/{team_id}/{player_id}.json', 'w') as data:
        json.dump(player_json, data, indent=4)


def extract_game_info(game_id, team_id, players, description):
    """
    Extract info from Game files
    :param game_id: Game string identifies, matches the files' name
    :param team_id: Team id  which the info is extracted
    :param players: Team players list
    :param description: HOMEDESCRIPTION or VISITORDESCRIPTION, string to search in the correct column
    depending if the Team are local or visitor
    :return: team_dict: dictionary with Team statistics extracted for the game's files, including Players statistics
    """
    players_list = []
    # Create dict to save Player info
    for player_json in players:
        player_dict = {
            'player_id': player_json['player_id'],
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
    game_data = pd.read_csv(f'gameAnalyzer/data/events/{game_id}.csv')

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
        player_made_shots = made_shots[made_shots['PLAYER1_ID'] == player['player_id']]
        # Load Player field goals made
        player_field_goals = player_made_shots.shape[0]
        # Load Player 3 field goals made
        player_3pt = player_made_shots[player_made_shots[description].str.contains('3PT')].shape[0]
        # Load Player assists
        player_assists = made_shots[made_shots['PLAYER2_ID'] == player['player_id']].shape[0]

        # Load Player missed shots
        player_misses = missed_shots[missed_shots['PLAYER1_ID'] == player['player_id']]
        # Load Player field goals misses.
        player_field_goals_misses = player_misses.shape[0]
        # Load Player 3 field goals made.
        player_3pt_misses = player_misses[player_misses[description].str.contains('3PT')].shape[0]

        extract_player_shots_coordinates(game_id, player['player_id'], team_id)

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
        player_personal_fouls = personal_fouls[personal_fouls['PLAYER1_ID'] == player['player_id']].shape[0]

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

            elif row['PLAYER2_ID'] == player['player_id']:
                # Player enters the game
                minutes = int(re.sub(':[0-9]*', '', row['PCTIMESTRING']))
                seconds = int(re.sub('[0-9]*:', '', row['PCTIMESTRING']))
                minutes_played += minutes * 60 + seconds

                last_quarter = row['PERIOD']

        # Check if Player record some event and we haven't sub or in event, so we add entire quarter time
        if (player_substitutions[player_substitutions['PERIOD'] == 1].shape[0] == 0) and \
                (game_data[(game_data['PERIOD'] == 1) & ((game_data['PLAYER1_ID'] == player['player_id'])
                                                         | (game_data['PLAYER2_ID'] == player['player_id'])
                                                         | (game_data['PLAYER3_ID'] == player['player_id']))]
                         .shape[0] > 0):
            minutes_played += 720

        if (player_substitutions[player_substitutions['PERIOD'] == 2].shape[0] == 0) and \
                (game_data[(game_data['PERIOD'] == 2) & ((game_data['PLAYER1_ID'] == player['player_id'])
                                                         | (game_data['PLAYER2_ID'] == player['player_id'])
                                                         | (game_data['PLAYER3_ID'] == player['player_id']))]
                         .shape[0] > 0):
            minutes_played += 720

        if (player_substitutions[player_substitutions['PERIOD'] == 3].shape[0] == 0) and \
                (game_data[(game_data['PERIOD'] == 3) & ((game_data['PLAYER1_ID'] == player['player_id'])
                                                         | (game_data['PLAYER2_ID'] == player['player_id'])
                                                         | (game_data['PLAYER3_ID'] == player['player_id']))]
                         .shape[0] > 0):
            minutes_played += 720

        if (player_substitutions[player_substitutions['PERIOD'] == 4].shape[0] == 0) and \
                (game_data[(game_data['PERIOD'] == 4) & ((game_data['PLAYER1_ID'] == player['player_id'])
                                                         | (game_data['PLAYER2_ID'] == player['player_id'])
                                                         | (game_data['PLAYER3_ID'] == player['player_id']))]
                         .shape[0] > 0):
            minutes_played += 720

        player['played_games'] = int(minutes_played > 0)
        player['scored_points'] = (player_field_goals - player_3pt) * 2 + player_3pt * 3 + player_free_throw_made
        player['played_minutes'] = minutes_played
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

    game_made_shots = game_data[game_data['EVENTMSGTYPE'] == 1]
    game_miss_shots = game_data[game_data['EVENTMSGTYPE'] == 2]
    defender_list = []
    defender_list += guess_defender(game_made_shots, 0, f'{game_id}.json')
    defender_list += guess_defender(game_miss_shots, 1, f'{game_id}.json')

    shooter_defender = pd.DataFrame(defender_list, columns=['Shooter ID', 'Defender ID', 'Defend Success'])
    insert_defend_data(shooter_defender)

    return team_dict
