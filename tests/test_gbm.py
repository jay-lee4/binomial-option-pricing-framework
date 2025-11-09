import pytest
import numpy as np
from src.gbm import GBM


class TestGBMInitialization:
    
    def test_valid_initialization(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        assert gbm.mu == 0.08
        assert gbm.sigma == 0.2
        assert gbm.n_steps == 100
        assert gbm.n_paths == 10
        assert gbm.S0 == 100
        assert gbm.T == 1.0
        assert gbm.dt == 0.01
    
    def test_invalid_initial_price(self):
        with pytest.raises(ValueError):
            GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=-100, T=1.0)
        
        with pytest.raises(ValueError):
            GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=0, T=1.0)
    
    def test_invalid_volatility(self):
        with pytest.raises(ValueError):
            GBM(mu=0.08, sigma=-0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
    
    def test_invalid_n_steps(self):
        with pytest.raises(ValueError):
            GBM(mu=0.08, sigma=0.2, n_steps=0, n_paths=10, S0=100, T=1.0)
        
        with pytest.raises(ValueError):
            GBM(mu=0.08, sigma=0.2, n_steps=-100, n_paths=10, S0=100, T=1.0)
    
    def test_invalid_n_paths(self):
        with pytest.raises(ValueError):
            GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=0, S0=100, T=1.0)
    
    def test_invalid_time_horizon(self):
        with pytest.raises(ValueError):
            GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=0)


class TestGBMPaths:
    
    def test_path_shape(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        paths = gbm.get_all_paths()
        assert paths.shape == (10, 101)
    
    def test_initial_prices(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        paths = gbm.get_all_paths()
        np.testing.assert_array_almost_equal(paths[:, 0], 100.0)
    
    def test_prices_positive(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        paths = gbm.get_all_paths()
        assert np.all(paths > 0)
    
    def test_different_seeds_different_paths(self):
        np.random.seed(42)
        gbm1 = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=5, S0=100, T=1.0)
        paths1 = gbm1.get_all_paths()
        
        np.random.seed(123)
        gbm2 = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=5, S0=100, T=1.0)
        paths2 = gbm2.get_all_paths()
        
        assert not np.array_equal(paths1, paths2)
    
    def test_same_seed_same_paths(self):
        np.random.seed(42)
        gbm1 = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=5, S0=100, T=1.0)
        paths1 = gbm1.get_all_paths()
        
        np.random.seed(42)
        gbm2 = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=5, S0=100, T=1.0)
        paths2 = gbm2.get_all_paths()
        
        np.testing.assert_array_almost_equal(paths1, paths2)


class TestGBMFinalPrices:
    
    def test_final_prices_shape(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        final_prices = gbm.get_final_prices()
        assert final_prices.shape == (10,)
    
    def test_final_prices_positive(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        final_prices = gbm.get_final_prices()
        assert np.all(final_prices > 0)
    
    def test_final_prices_match_paths(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        paths = gbm.get_all_paths()
        final_prices = gbm.get_final_prices()
        np.testing.assert_array_equal(final_prices, paths[:, -1])
    
    def test_zero_volatility_deterministic(self):
        """Zero volatility should give deterministic growth."""
        gbm = GBM(mu=0.05, sigma=0.0, n_steps=100, n_paths=5, S0=100, T=1.0)
        final_prices = gbm.get_final_prices()
        
        expected = 100 * np.exp(0.05 * 1.0)
        np.testing.assert_array_almost_equal(final_prices, expected, decimal=5)
