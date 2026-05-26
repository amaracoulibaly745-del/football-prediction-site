import pytest
import pandas as pd
import numpy as np
from ml.model import FootballPredictionModel

class TestFootballPredictionModel:
    
    @pytest.fixture
    def model(self):
        return FootballPredictionModel()
    
    def test_model_initialization(self, model):
        assert model.model is None
        assert model.scaler is not None
    
    def test_prepare_features(self, model):
        match_data = {
            'team1': 'Manchester United',
            'team2': 'Liverpool',
            'date': '2024-01-01',
            'referee': 'Michael Oliver'
        }
        
        features = model.prepare_features(match_data)
        assert features.shape[0] == 1  # Un match
    
    def test_prediction_without_training(self, model):
        match_data = {'team1': 'Team A', 'team2': 'Team B'}
        result = model.predict(match_data)
        assert result == {}
