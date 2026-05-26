import pandas as pd
import numpy as np
from loguru import logger
from typing import Dict, Tuple

class DataProcessor:
    """
    Traite et nettoie les données de football
    """
    
    def __init__(self):
        logger.info("Initialisation du processeur de données")
    
    def clean_matches_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoyer et préparer les données de matchs
        """
        if df.empty:
            logger.warning("DataFrame vide")
            return df
        
        # Supprimer les doublons
        df = df.drop_duplicates()
        
        # Remplir les valeurs manquantes
        df = df.fillna(0)
        
        # Convertir les types de données
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        logger.info(f"Données de matchs nettoyées: {len(df)} lignes")
        return df
    
    def calculate_team_stats(self, matches_df: pd.DataFrame, team_name: str) -> Dict:
        """
        Calculer les statistiques d'une équipe
        """
        # Matchs où l'équipe joue à domicile
        home_matches = matches_df[matches_df['home_team'] == team_name]
        # Matchs où l'équipe joue à l'extérieur
        away_matches = matches_df[matches_df['away_team'] == team_name]
        
        stats = {
            'team_name': team_name,
            'total_matches': len(home_matches) + len(away_matches),
            'home_matches': len(home_matches),
            'away_matches': len(away_matches),
            'avg_goals_for': 0,
            'avg_goals_against': 0,
            'win_percentage': 0,
            'recent_form': []  # Derniers 5 matchs
        }
        
        return stats
    
    def prepare_training_data(self, matches_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Préparer les données pour l'entraînement du modèle ML
        
        Returns:
            X: Features
            y: Target (résultat du match)
        """
        if matches_df.empty:
            return pd.DataFrame(), pd.Series()
        
        # Créer les features
        X = matches_df[[]]  # À compléter avec les features pertinentes
        
        # Créer la target (0: défaite, 1: victoire, 2: nul)
        y = matches_df['result'] if 'result' in matches_df.columns else pd.Series()
        
        logger.info(f"Données d'entraînement préparées: {len(X)} échantillons")
        return X, y
    
    def enrich_with_referee_data(self, matches_df: pd.DataFrame, referees_df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrichir les données de matchs avec les informations des arbitres
        """
        if matches_df.empty or referees_df.empty:
            return matches_df
        
        # Fusionner sur l'arbitre
        if 'referee' in matches_df.columns and 'name' in referees_df.columns:
            matches_df = matches_df.merge(
                referees_df,
                left_on='referee',
                right_on='name',
                how='left'
            )
        
        logger.info(f"Données enrichies avec les infos d'arbitres")
        return matches_df
    
    def calculate_referee_impact_score(self, matches_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculer un score d'impact pour chaque arbitre
        """
        if 'referee' not in matches_df.columns:
            return matches_df
        
        referee_impact = matches_df.groupby('referee').agg({
            'yellow_cards': 'mean',
            'red_cards': 'mean',
            'penalties': 'mean'
        }).reset_index()
        
        # Créer un score d'impact (0-1)
        referee_impact['impact_score'] = (
            (referee_impact['yellow_cards'] / 4) +
            (referee_impact['red_cards'] / 1) +
            (referee_impact['penalties'] / 1)
        ) / 3
        
        return referee_impact
