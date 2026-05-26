import requests
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

class FootballDataCollector:
    """
    Collecte les données de football depuis diverses APIs
    """
    
    def __init__(self):
        self.api_key = os.getenv('FOOTBALL_API_KEY')
        self.base_url = 'https://v3.football.api-sports.io'
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'api-sports.io'
        }
        logger.info("Initialisation du collecteur de données")
    
    def fetch_matches(self, league_id: int, season: int) -> pd.DataFrame:
        """
        Récupérer les matchs d'une ligue pour une saison
        """
        endpoint = f"{self.base_url}/fixtures"
        params = {
            'league': league_id,
            'season': season
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            matches = response.json().get('response', [])
            logger.info(f"Récupéré {len(matches)} matchs")
            
            return pd.DataFrame(matches)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des matchs: {str(e)}")
            return pd.DataFrame()
    
    def fetch_teams(self, league_id: int, season: int) -> pd.DataFrame:
        """
        Récupérer les équipes d'une ligue
        """
        endpoint = f"{self.base_url}/standings"
        params = {
            'league': league_id,
            'season': season
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            standings = response.json().get('response', [])
            teams_list = []
            
            for league_data in standings:
                for team_data in league_data.get('league', {}).get('standings', [[]])[0]:
                    teams_list.append(team_data['team'])
            
            logger.info(f"Récupéré {len(teams_list)} équipes")
            return pd.DataFrame(teams_list)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des équipes: {str(e)}")
            return pd.DataFrame()
    
    def fetch_referees(self) -> pd.DataFrame:
        """
        Récupérer les données des arbitres
        """
        endpoint = f"{self.base_url}/referees"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            
            referees = response.json().get('response', [])
            logger.info(f"Récupéré {len(referees)} arbitres")
            
            return pd.DataFrame(referees)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des arbitres: {str(e)}")
            return pd.DataFrame()
    
    def fetch_player_stats(self, player_id: int, season: int) -> dict:
        """
        Récupérer les statistiques d'un joueur
        """
        endpoint = f"{self.base_url}/players"
        params = {
            'id': player_id,
            'season': season
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json().get('response', {})
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats du joueur: {str(e)}")
            return {}
    
    def collect_all_data(self, league_id: int = 39, season: int = 2024):
        """
        Collecter toutes les données nécessaires
        """
        logger.info(f"Collecte de toutes les données pour la ligue {league_id}, saison {season}")
        
        data = {
            'matches': self.fetch_matches(league_id, season),
            'teams': self.fetch_teams(league_id, season),
            'referees': self.fetch_referees()
        }
        
        return data
