import pytest
import numpy as np
from src.analytics import (
    exp_profits,
    CoxRossRubinsteinRW,
    SteveShreveRW,
    DriftAdjustedRW
)


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


class TestCoxRossRubinsteinRW:
    
    def test_initialization(self):
        rw = CoxRossRubinsteinRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        assert rw.model == "Cox-Ross-Rubinstein"
        assert rw.u_star > 1.0
        assert rw.d_start < 1.0
    
    def test_prob_profit_bounds(self):
        rw = CoxRossRubinsteinRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        prob = rw.get_prob_profit()
        assert 0 <= prob <= 1
    
    def test_exp_profits(self):
        rw = CoxRossRubinsteinRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        exp_profit = rw.get_exp_profits(initial_capital=5.0)
        assert isinstance(exp_profit, (float, np.floating))
    
    def test_get_probs_sum_to_one(self):
        rw = CoxRossRubinsteinRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        probs = rw.get_probs()
        from src.utils import n_choose
        freq_list = n_choose(rw.N) * probs
        assert abs(np.sum(freq_list) - 1.0) < 1e-10


class TestSteveShreveRW:
    
    def test_initialization(self):
        rw = SteveShreveRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        assert rw.model == "Steve Shreve"
        assert rw.u_star > 1.0
        assert rw.d_start < 1.0
    
    def test_prob_profit_bounds(self):
        rw = SteveShreveRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        prob = rw.get_prob_profit()
        assert 0 <= prob <= 1
    
    def test_exp_profits(self):
        rw = SteveShreveRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        exp_profit = rw.get_exp_profits(initial_capital=5.0)
        assert isinstance(exp_profit, (float, np.floating))


class TestDriftAdjustedRW:
    
    def test_initialization(self):
        rw = DriftAdjustedRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        assert rw.model == "Drift-Adjusted"
        assert rw.u_star > 1.0
        assert rw.d_start < 1.0
    
    def test_prob_profit_bounds(self):
        rw = DriftAdjustedRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        prob = rw.get_prob_profit()
        assert 0 <= prob <= 1
    
    def test_exp_profits(self):
        rw = DriftAdjustedRW(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        exp_profit = rw.get_exp_profits(initial_capital=5.0)
        assert isinstance(exp_profit, (float, np.floating))
    
    def test_uses_mu_not_r(self):
        """Drift-adjusted should use mu in tree construction."""
        rw = DriftAdjustedRW(
            S=100, m=0.10, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        
        # With mu=0.10, factors should be different than with r=0.05
        temp = rw.sigma * np.sqrt(rw.T / rw.N)
        temp2 = 1 + rw.m * (rw.T / rw.N)
        expected_u = temp2 + temp
        
        assert abs(rw.u_star - expected_u) < 1e-10


class TestModelComparison:
    
    def test_all_models_give_different_results(self):
        """Different models should give different probability estimates."""
        params = dict(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        
        crr = CoxRossRubinsteinRW(**params)
        shreve = SteveShreveRW(**params)
        drift = DriftAdjustedRW(**params)
        
        prob_crr = crr.get_prob_profit()
        prob_shreve = shreve.get_prob_profit()
        prob_drift = drift.get_prob_profit()
        
        # At least two should be different
        assert not (prob_crr == prob_shreve == prob_drift)
    
    def test_all_models_positive_exp_profit_high_capital(self):
        """High initial capital should give positive expected profit for all models."""
        params = dict(
            S=100, m=0.08, r=0.05, sigma=0.2,
            T=1.0, N=100, K1=90, K2=95, K3=105, K4=110
        )
        
        crr = CoxRossRubinsteinRW(**params)
        shreve = SteveShreveRW(**params)
        drift = DriftAdjustedRW(**params)
        
        assert crr.get_exp_profits(initial_capital=50.0) > 0
        assert shreve.get_exp_profits(initial_capital=50.0) > 0
        assert drift.get_exp_profits(initial_capital=50.0) > 0
