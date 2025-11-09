import pytest
import numpy as np
from src.models import cox_ross_rubinstein


class TestCoxRossRubinstein:
    
    def test_call_option_itm(self):
        """In-the-money call should have positive value."""
        price = cox_ross_rubinstein(
            S=110, K=100, T=1.0, r=0.05, sigma=0.2, N=100, option_type='C'
        )
        assert price > 10.0
        assert price < 20.0
    
    def test_call_option_otm(self):
        """Out-of-the-money call should have small positive value."""
        price = cox_ross_rubinstein(
            S=90, K=100, T=1.0, r=0.05, sigma=0.2, N=100, option_type='C'
        )
        assert price > 0
        assert price < 6.0
    
    def test_put_option_itm(self):
        """In-the-money put should have positive value."""
        price = cox_ross_rubinstein(
            S=90, K=100, T=1.0, r=0.05, sigma=0.2, N=100, option_type='P'
        )
        assert price > 5.0
        assert price < 15.0
    
    def test_put_option_otm(self):
        """Out-of-the-money put should have small positive value."""
        price = cox_ross_rubinstein(
            S=110, K=100, T=1.0, r=0.05, sigma=0.2, N=100, option_type='P'
        )
        assert price > 0
        assert price < 3.0
    
    def test_put_call_parity(self):
        """Test put-call parity: C - P = S - K*exp(-rT)."""
        S, K, T, r = 100, 100, 1.0, 0.05
        sigma, N = 0.2, 200
        
        call = cox_ross_rubinstein(S, K, T, r, sigma, N, 'C')
        put = cox_ross_rubinstein(S, K, T, r, sigma, N, 'P')
        
        lhs = call - put
        rhs = S - K * np.exp(-r * T)
        
        assert abs(lhs - rhs) < 0.1
    
    def test_increasing_steps_convergence(self):
        """More time steps should converge to stable price."""
        S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2
        
        price_100 = cox_ross_rubinstein(S, K, T, r, sigma, 100, 'C')
        price_500 = cox_ross_rubinstein(S, K, T, r, sigma, 500, 'C')
        
        assert abs(price_100 - price_500) < 0.5
    
    def test_low_volatility_call(self):
        """Low volatility deep ITM call should approximate intrinsic value."""
        S, K = 110, 100
        price = cox_ross_rubinstein(
            S=S, K=K, T=1.0, r=0.05, sigma=0.05, N=100, option_type='C'
        )
        intrinsic = S - K * np.exp(-0.05 * 1.0)
        assert abs(price - intrinsic) < 2.0
    
    def test_invalid_option_type(self):
        """Invalid option type should raise ValueError."""
        with pytest.raises(ValueError):
            cox_ross_rubinstein(
                S=100, K=100, T=1.0, r=0.05, sigma=0.2, N=100, option_type='X'
            )
    
    def test_known_value(self):
        """Test against a known reference value."""
        price = cox_ross_rubinstein(
            S=100, K=100, T=1.0, r=0.05, sigma=0.2, N=1000, option_type='C'
        )
        assert 9.5 < price < 11.5
