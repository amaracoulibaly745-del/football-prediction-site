import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import pickle
from loguru import logger

class FootballPredictionModel:
    """
    Modèle ML pour prédire les résultats de matchs de football
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        logger.info("Initialisation du modèle de prédiction")
    
    def prepare_features(self, match_data: dict) -> np.ndarray:
        """
        Préparer les features pour le modèle
        
        Features:
        - Team 1 strength
        - Team 2 strength
        - Home advantage
        - Recent form team 1
        - Recent form team 2
        - Referee tendency
        - Weather conditions
        - Head to head history
        """
        features = []
        
        # À implémenter avec les données réelles
        self.feature_names = [
            'team1_strength',
            'team2_strength',
            'home_advantage',
            'team1_form',
            'team2_form',
            'referee_tendency',
            'weather',
            'h2h_advantage'
        ]
        
        return np.array(features).reshape(1, -1)
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Entraîner le modèle
        """
        logger.info(f"Entraînement du modèle avec {len(X_train)} échantillons")
        
        # Normaliser les données
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Utiliser GradientBoosting pour de meilleures performances
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        self.model.fit(X_scaled, y_train)
        logger.info("Modèle entraîné avec succès")
    
    def predict(self, match_data: dict) -> dict:
        """
        Prédire le résultat d'un match
        
        Returns:
        {
            'prediction': '1' | '0' | '2',  # Victoire équipe 1, nul, victoire équipe 2
            'confidence': float,
            'probabilities': {'1': float, '0': float, '2': float}
        }
        """
        if self.model is None:
            logger.error("Modèle non entraîné")
            return {}
        
        features = self.prepare_features(match_data)
        features_scaled = self.scaler.transform(features)
        
        # Prédiction
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = max(probabilities)
        
        result_map = {0: '2', 1: '1', 2: '0'}  # 0: defaite, 1: victoire, 2: nul
        
        return {
            'prediction': result_map[prediction],
            'confidence': float(confidence),
            'probabilities': {
                'team1_win': float(probabilities[1]),
                'draw': float(probabilities[2]),
                'team2_win': float(probabilities[0])
            }
        }
    
    def save(self, filepath: str):
        """
        Sauvegarder le modèle
        """
        with open(filepath, 'wb') as f:
            pickle.dump((self.model, self.scaler, self.feature_names), f)
        logger.info(f"Modèle sauvegardé à {filepath}")
    
    def load(self, filepath: str):
        """
        Charger le modèle
        """
        with open(filepath, 'rb') as f:
            self.model, self.scaler, self.feature_names = pickle.load(f)
        logger.info(f"Modèle chargé depuis {filepath}")
