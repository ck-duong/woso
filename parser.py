import pandas as pd
import os
import json
import requests
from pandas.io.json import json_normalize

BASE_URL = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data'

class Competitions:
    """
    Parses data/competitions.json into a csv format
    """
    def __init__(self):
        self.path = f'{BASE_URL}/competitions.json'
        
    def __repr__(self):
        return 'Competition Data Parser'
        
    def get_data(self):
        self.data = requests.get(self.path).json()
        return pd.DataFrame(self.data)
    
class Matches:
    """
    Parses data/matches
    """
    def __init__(self, competition_id, season_id):
        self.comp = str(competition_id)
        self.season = str(season_id)
        self.path = f'{BASE_URL}/matches/{self.comp}/{self.season}.json'
        self.data = requests.get(self.path).json()
    
    def get_data(self):
        return json_normalize(self.data)
    
class Lineups:
    """
    Parses data/lineups
    """
    def __init__(self, match_id):
        self.comp = str(match_id)
        self.path = f'{BASE_URL}/lineups/{self.comp}.json'
        self.data = requests.get(self.path).json()
    
    def define_home(self):
        return {'home_id': self.data[0]['team_id'],
                'home_name': self.data[0]['team_name']}
    
    def define_away(self):
        return {'away_id': self.data[1]['team_id'],
                'away_name': self.data[1]['team_name']}
    
    def get_data(self): 
        home_team = json_normalize(self.data[0]['lineup'])
        home = self.define_home()
        home_team['team_id'] = home['home_id']
        home_team['team_name'] = home['home_name']
        
        away_team = json_normalize(self.data[1]['lineup'])
        away = self.define_away()
        away_team['team_id'] = away['away_id']
        away_team['team_name'] = away['away_name']
        
        return pd.concat([home_team, away_team])
    
class Events:
    """
    Parses data/events
    """
    def __init__(self, match_id):
        self.comp = str(match_id)
        self.path = f'{BASE_URL}/events/{self.comp}.json'
        self.data = requests.get(self.path).json()
    
    def print_action_types(self):
        unique_actions = []
        for event in self.data:
            if event['type']['name'] not in unique_actions:
                unique_actions.append(event['type']['name'])
        return unique_actions
    
    def print_players(self):
        unique_players = []
        for event in self.data:
            try:
                name = event['player']['name']
                if name not in unique_players:
                    unique_players.append(name)
            except:
                pass
        return unique_players
    
    def get_player_data(self, player_name):
        valid_actions = []
        for event in self.data:
            try:
                if event['player']['name'] == player_name:
                    valid_actions.append(event)
            except:
                pass
        return json_normalize(valid_actions)
        
    def get_action_data(self, action_type = 'Pass'):
        valid_actions = []
        for event in self.data:
            if event['type']['name'] == action_type:
                valid_actions.append(event)
        return json_normalize(valid_actions)
        
                