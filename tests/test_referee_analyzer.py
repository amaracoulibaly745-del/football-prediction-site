import pytest
import pandas as pd
from ml.referee_analyzer import RefereeAnalyzer

class TestRefereeAnalyzer:
    
    @pytest.fixture
    def analyzer(self):
        return RefereeAnalyzer()
    
    @pytest.fixture
    def sample_referee_data(self):
        return pd.DataFrame({
            'match_id': [1, 2, 3, 4, 5],
            'yellow_cards': [4, 5, 3, 6, 4],
            'red_cards': [0, 1, 0, 0, 1],
            'penalties': [1, 2, 1, 2, 1],
            'corners': [10, 12, 11, 13, 10],
            'home_favorable_decisions': [2, 3, 2, 4, 2]
        })
    
    def test_analyze_referee(self, analyzer, sample_referee_data):
        stats = analyzer.analyze_referee('Michael Oliver', sample_referee_data)
        
        assert stats['referee_name'] == 'Michael Oliver'
        assert stats['total_matches'] == 5
        assert stats['avg_yellow_cards'] == 4.4
        assert 0 <= stats['consistency_score'] <= 1
