import pandas as pd

from dataBaseManager.apps import DatabasemanagerConfig
from dataBaseManager.models import Player


def insert_defend_data(shooter_defender):
    data = pd.read_csv('dataBaseManager/data/Defend-data.csv')
    shooter_cluster = []
    defender_cluster = []
    shooter_position = []
    defender_position = []
    for ind, row in shooter_defender:
        shooter = Player.objects.get(row['Shooter ID'].values[0])
        defender = Player.objects.get(row['Defender ID'].values[0])
        shooter_cluster.append(shooter.cluster)
        defender_cluster.append(defender.cluster)
        shooter_position.append(shooter.position)
        defender_position.append(defender.position)

    shooter_defender['Shooter position'] = shooter_position
    shooter_defender['Defender position'] = defender_position
    shooter_defender['Shooter Cluster'] = shooter_cluster
    shooter_defender['Defender Cluster'] = defender_cluster
    data.append(shooter_defender)
    data.to_csv('dataBaseManager/data/Defend-data.csv')
    DatabasemanagerConfig.defend_data = pd.read_csv('dataBaseManager/data/Defend-data.csv')
