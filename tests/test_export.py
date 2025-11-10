import pytest
import json
from src.export import (
    export_results_to_csv,
    export_parameters_to_json,
    export_optimization_to_csv,
    export_simulation_data_to_csv
)
import numpy as np


class TestExportResultsToCSV:
    
    def test_returns_dataframe(self):
        results = {
            'CRR': {
                'K1': 1.5,
                'K2': 3.0,
                'K3': 2.5,
                'K4': 1.0,
                'Initial Capital': 5.0,
                'GBM Expected Value': 2.5,
                'RW Expected Value': 2.8,
                'Probability of Profit': 0.65
            },
            'Steve Shreve': {
                'K1': 1.5,
                'K2': 3.0,
                'K3': 2.5,
                'K4': 1.0,
                'Initial Capital': 5.1,
                'GBM Expected Value': 2.6,
                'RW Expected Value': 2.9,
                'Probability of Profit': 0.66
            },
            'Drift-Adjusted': {
                'K1': 1.6,
                'K2': 3.1,
                'K3': 2.6,
                'K4': 1.1,
                'Initial Capital': 5.2,
                'GBM Expected Value': 2.7,
                'RW Expected Value': 3.0,
                'Probability of Profit': 0.67
            }
        }
        
        inputs = {'S': 100, 'K1': 90, 'K2': 95, 'K3': 105, 'K4': 110}
        
        df = export_results_to_csv(results, inputs)
        
        assert len(df) == 3
        assert 'Model' in df.columns
        assert 'Initial_Capital' in df.columns


class TestExportParametersToJSON:
    
    def test_returns_valid_json(self):
        inputs = {
            'strategy': 'Iron Condor',
            'S': 100.0,
            'K1': 90.0,
            'K2': 95.0,
            'K3': 105.0,
            'K4': 110.0,
            'r': 0.05,
            'mu': 0.08,
            'sigma': 0.2,
            'T': 1.0,
            'N': 100,
            'n_paths': 1000
        }
        
        json_str = export_parameters_to_json(inputs)
        
        # Should be valid JSON
        data = json.loads(json_str)
        
        assert 'timestamp' in data
        assert 'parameters' in data
        assert data['parameters']['strategy'] == 'Iron Condor'
