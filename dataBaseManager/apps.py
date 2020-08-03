from django.apps import AppConfig
import pandas as pd


class DatabasemanagerConfig(AppConfig):
    name = 'dataBaseManager'
    defend_data = pd.read_csv('dataBaseManager/Data/Defend-data.csv')
