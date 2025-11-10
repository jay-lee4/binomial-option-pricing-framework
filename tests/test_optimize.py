import pytest
import numpy as np
from src.optimize import (
    calculate_initial_capitals,
    strike_to_profit_gbm,
    generate_strike_grid,
    optimize_strikes
)


class TestCalculateInitialCapitals:
    
    def test_returns_dict(self):
        result = calculate_initial_capitals(
            S=100, K1=90, K2=95, K3=105, K4=110,
            T=1.0, r=0.05, sigma=0.2, mu=0.08, N=100
        )
        assert isinstance(result, dict)
        assert 'CRR' in result
        assert 'Steve Shreve' in result
        assert 'Drift-Adjusted' in result
    
    def test_positive_initial_capital(self):
        result = calculate_initial_capitals(
            S=100, K1=90, K2=95, K3=105, K4=110,
            T=1.0, r=0.05, sigma=0.2, mu=0.08, N=100
        )
        # Iron Condor should typically have positive initial capital
        assert result['CRR'] > 0


class TestStrikeToProfitGBM:
    
    def test_basic_calculation(self):
        final_prices = np.array([95, 100, 105, 110, 115])
        profit = strike_to_profit_gbm(
            K1=90, K2=95, K3=105, K4=110,
            final_prices=final_prices,
            initial_capital=5.0,
            payout_name='iron_condor'
        )
        assert isinstance(profit, (float, np.floating))


class TestGenerateStrikeGrid:
    
    def test_small_grid(self):
        grid = generate_strike_grid(S=100, grid_size='small')
        assert len(grid) > 0
        assert all(isinstance(strikes, tuple) for strikes in grid)
        assert all(len(strikes) == 4 for strikes in grid)
    
    def test_medium_grid_larger_than_small(self):
        small_grid = generate_strike_grid(S=100, grid_size='small')
        medium_grid = generate_strike_grid(S=100, grid_size='medium')
        assert len(medium_grid) >= len(small_grid)
    
    def test_valid_strike_ordering(self):
        grid = generate_strike_grid(S=100, grid_size='small')
        for k1, k2, k3, k4 in grid:
            assert k1 < k2 < k3 < k4


class TestOptimizeStrikes:
    
    def test_returns_results_dict(self):
        np.random.seed(42)
        final_prices = np.random.lognormal(mean=np.log(100), sigma=0.2, size=100)
        
        results = optimize_strikes(
            S=100, r=0.05, T=1.0, sigma=0.2, mu=0.08,
            final_prices=final_prices,
            N=50,
            grid_size='small',
            payout_name='iron_condor'
        )
        
        assert 'CRR' in results
        assert 'Steve Shreve' in results
        assert 'Drift-Adjusted' in results
        
        assert results['CRR']['GBM_optimal_strikes'] is not None
        assert results['CRR']['RW_optimal_strikes'] is not None
