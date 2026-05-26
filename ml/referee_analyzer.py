import pandas as pd
import numpy as np
from typing import Dict, List
from loguru import logger

class RefereeAnalyzer:
    """
    Analyse l'impact et les tendances des arbitres
    """
    
    def __init__(self):
        self.referee_stats = {}
        logger.info("Initialisation de l'analyseur d'arbitres")
    
    def analyze_referee(self, referee_name: str, matches_data: pd.DataFrame) -> Dict:
        """
        Analyser les statistiques et tendances d'un arbitre
        
        Args:
            referee_name: Nom de l'arbitre
            matches_data: DataFrame avec les matchs arbitrés par ce referee
        
        Returns:
            Dict avec les statistiques du referee
        """
        if matches_data.empty:
            logger.warning(f"Aucune donnée pour {referee_name}")
            return {}
        
        stats = {
            'referee_name': referee_name,
            'total_matches': len(matches_data),
            'avg_yellow_cards': matches_data['yellow_cards'].mean() if 'yellow_cards' in matches_data else 0,
            'avg_red_cards': matches_data['red_cards'].mean() if 'red_cards' in matches_data else 0,
            'avg_penalties': matches_data['penalties'].mean() if 'penalties' in matches_data else 0,
            'avg_corners': matches_data['corners'].mean() if 'corners' in matches_data else 0,
            'home_bias': self._calculate_home_bias(matches_data),
            'tendency_score': self._calculate_tendency_score(matches_data),
            'consistency_score': self._calculate_consistency(matches_data)
        }
        
        self.referee_stats[referee_name] = stats
        return stats
    
    def _calculate_home_bias(self, matches_data: pd.DataFrame) -> float:
        """
        Calculer le biais en faveur de l'équipe domicile
        """
        if len(matches_data) < 2:
            return 0.0
        
        # Analyser les décisions en faveur de l'équipe domicile
        home_favorable = matches_data['home_favorable_decisions'].sum() if 'home_favorable_decisions' in matches_data else 0
        return home_favorable / len(matches_data)
    
    def _calculate_tendency_score(self, matches_data: pd.DataFrame) -> float:
        """
        Score de tendance générale de l'arbitre (strict vs permissif)
        """
        # Score basé sur les cartons et pénalties
        yellow = matches_data['yellow_cards'].sum() if 'yellow_cards' in matches_data else 0
        red = matches_data['red_cards'].sum() if 'red_cards' in matches_data else 0
        
        strictness = (yellow + red * 2) / max(len(matches_data), 1)
        return min(strictness / 10, 1.0)  # Normaliser entre 0 et 1
    
    def _calculate_consistency(self, matches_data: pd.DataFrame) -> float:
        """
        Calculer la cohérence des décisions de l'arbitre
        """
        if len(matches_data) < 2:
            return 0.0
        
        yellow_std = matches_data['yellow_cards'].std() if 'yellow_cards' in matches_data else 0
        # Plus l'écart-type est faible, plus l'arbitre est cohérent
        consistency = 1 / (1 + yellow_std)
        return min(consistency, 1.0)
    
    def compare_referees(self, referee_list: List[str]) -> pd.DataFrame:
        """
        Comparer plusieurs arbitres
        """
        data = []
        for referee in referee_list:
            if referee in self.referee_stats:
                data.append(self.referee_stats[referee])
        
        return pd.DataFrame(data)
    
    def predict_referee_impact(self, referee_name: str, match_data: Dict) -> Dict:
        """
        Prédire l'impact potentiel d'un arbitre sur un match
        """
        if referee_name not in self.referee_stats:
            logger.warning(f"Statistiques manquantes pour {referee_name}")
            return {}
        
        ref_stats = self.referee_stats[referee_name]
        
        return {
            'referee_name': referee_name,
            'expected_yellow_cards': ref_stats['avg_yellow_cards'],
            'expected_red_cards': ref_stats['avg_red_cards'],
            'expected_penalties': ref_stats['avg_penalties'],
            'home_bias_risk': ref_stats['home_bias'],
            'strictness_level': 'Strict' if ref_stats['tendency_score'] > 0.6 else 'Normal' if ref_stats['tendency_score'] > 0.4 else 'Permissif'
        }
