import pytest
from src.validation import (
    validate_strike_prices,
    validate_market_parameters,
    validate_simulation_parameters,
    validate_stock_price,
    validate_all_inputs
)


class TestValidateStrikePrices:
    
    def test_valid_iron_condor(self):
        is_valid, error = validate_strike_prices(90, 95, 105, 110, 100, "Iron Condor")
        assert is_valid
        assert error is None
    
    def test_invalid_ordering(self):
        is_valid, error = validate_strike_prices(95, 90, 105, 110, 100, "Iron Condor")
        assert not is_valid
        assert "K1 < K2 < K3 < K4" in error
    
    def test_k2_above_stock_price(self):
        is_valid, error = validate_strike_prices(90, 105, 110, 115, 100, "Iron Condor")
        assert not is_valid
        assert "below current stock price" in error


class TestValidateMarketParameters:
    
    def test_valid_parameters(self):
        is_valid, error = validate_market_parameters(0.05, 0.08, 0.20, 1.0)
        assert is_valid
        assert error is None
    
    def test_negative_rate(self):
        is_valid, error = validate_market_parameters(-0.05, 0.08, 0.20, 1.0)
        assert not is_valid
        assert "negative" in error.lower()
    
    def test_zero_volatility(self):
        is_valid, error = validate_market_parameters(0.05, 0.08, 0.0, 1.0)
        assert not is_valid
        assert "positive" in error.lower()
    
    def test_negative_time(self):
        is_valid, error = validate_market_parameters(0.05, 0.08, 0.20, -1.0)
        assert not is_valid
        assert "positive" in error.lower()


class TestValidateSimulationParameters:
    
    def test_valid_parameters(self):
        is_valid, error = validate_simulation_parameters(100, 1000)
        assert is_valid
        assert error is None
    
    def test_too_few_steps(self):
        is_valid, error = validate_simulation_parameters(5, 1000)
        assert not is_valid
        assert "too low" in error
    
    def test_too_few_paths(self):
        is_valid, error = validate_simulation_parameters(100, 50)
        assert not is_valid
        assert "too low" in error


class TestValidateStockPrice:
    
    def test_valid_price(self):
        is_valid, error = validate_stock_price(100.0)
        assert is_valid
        assert error is None
    
    def test_negative_price(self):
        is_valid, error = validate_stock_price(-50.0)
        assert not is_valid
        assert "positive" in error.lower()
    
    def test_zero_price(self):
        is_valid, error = validate_stock_price(0.0)
        assert not is_valid
        assert "positive" in error.lower()


class TestValidateAllInputs:
    
    def test_valid_inputs(self):
        inputs = {
            'S': 100.0,
            'K1': 90.0,
            'K2': 95.0,
            'K3': 105.0,
            'K4': 110.0,
            'r': 0.05,
            'mu': 0.08,
            'sigma': 0.20,
            'T': 1.0,
            'N': 100,
            'n_paths': 1000,
            'strategy': 'Iron Condor'
        }
        
        is_valid, error = validate_all_inputs(inputs)
        assert is_valid
        assert error is None
