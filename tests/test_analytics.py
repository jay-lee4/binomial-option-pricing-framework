import pytest
import numpy as np
from src.analytics import exp_profits


class TestExpProfits:
    
    def test_basic_calculation(self):
        """Basic expected profit calculation should return a number."""
        result = exp_profits(
            S=100, n=50, u_star=1.02, d_start=0.98, p=0.5,
            K1=90, K2=95, K3=105, K4=110,
            initial_capital=5.0,
            payout_name="iron_condor"
        )
        assert isinstance(result, (float, np.floating))
    
    def test_high_initial_capital_positive_profit(self):
        """Very high initial capital should give positive expected profit."""
        result = exp_profits(
            S=100, n=50, u_star=1.01, d_start=0.99, p=0.5,
            K1=90, K2=95, K3=105, K4=110,
            initial_capital=100.0,
            payout_name="iron_condor"
        )
        assert result > 0
    
    def test_zero_initial_capital_negative_profit(self):
        """Zero initial capital should give negative expected profit."""
        result = exp_profits(
            S=100, n=50, u_star=1.02, d_start=0.98, p=0.5,
            K1=90, K2=95, K3=105, K4=110,
            initial_capital=0.0,
            payout_name="iron_condor"
        )
        assert result < 0
    
    def test_straddle_strategy(self):
        """Should handle straddle strategy."""
        result = exp_profits(
            S=100, n=50, u_star=1.02, d_start=0.98, p=0.5,
            K1=100, K2=95, K3=105, K4=110,
            initial_capital=10.0,
            payout_name="straddle"
        )
        assert isinstance(result, (float, np.floating))
    
    def test_strangle_strategy(self):
        """Should handle strangle strategy."""
        result = exp_profits(
            S=100, n=50, u_star=1.02, d_start=0.98, p=0.5,
            K1=95, K2=105, K3=105, K4=110,
            initial_capital=8.0,
            payout_name="strangle"
        )
        assert isinstance(result, (float, np.floating))
    
    def test_different_probabilities(self):
        """Different probabilities should give different expected profits."""
        params = dict(
            S=100, n=50, u_star=1.02, d_start=0.98,
            K1=90, K2=95, K3=105, K4=110,
            initial_capital=5.0,
            payout_name="iron_condor"
        )
        
        result_low_p = exp_profits(**params, p=0.3)
        result_high_p = exp_profits(**params, p=0.7)
        
        assert result_low_p != result_high_p
    
    def test_probabilities_sum_to_one(self):
        """Verify that probabilities across all states sum to ~1."""
        n = 100
        p = 0.5
        q = 1 - p
        range_ = np.arange(n + 1)
        
        probs = (p ** (n - range_)) * (q ** range_)
        from src.utils import n_choose
        freq_list = n_choose(n) * probs
        
        assert abs(np.sum(freq_list) - 1.0) < 1e-10


class TestRWProbsBase:
    
    def test_cannot_instantiate_abstract_class(self):
        """Cannot instantiate abstract RWProbs class directly."""
        from src.analytics import RWProbs
        
        with pytest.raises(TypeError):
            RWProbs(
                model="test", S=100, m=0.08, r=0.05, sigma=0.2,
                T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
            )
