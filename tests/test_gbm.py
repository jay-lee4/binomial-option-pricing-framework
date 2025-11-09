import pytest
import numpy as np
import pandas as pd
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
        gbm = GBM(mu=0.05, sigma=0.0, n_steps=100, n_paths=5, S0=100, T=1.0)
        final_prices = gbm.get_final_prices()
        
        expected = 100 * np.exp(0.05 * 1.0)
        np.testing.assert_array_almost_equal(final_prices, expected, decimal=5)


class TestGBMDataFrame:
    
    def test_to_dataframe_shape(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        df = gbm.to_dataframe()
        assert df.shape == (101, 10)
    
    def test_to_dataframe_index(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=10, S0=100, T=1.0)
        df = gbm.to_dataframe()
        assert df.index.name == "Time"
        assert df.index[0] == 0.0
        assert df.index[-1] == 1.0
    
    def test_to_dataframe_columns(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=5, S0=100, T=1.0)
        df = gbm.to_dataframe()
        expected_columns = ["Path_1", "Path_2", "Path_3", "Path_4", "Path_5"]
        assert list(df.columns) == expected_columns
    
    def test_to_dataframe_values_match_paths(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=5, S0=100, T=1.0)
        paths = gbm.get_all_paths()
        df = gbm.to_dataframe()
        np.testing.assert_array_almost_equal(df.values, paths.T)
    
    def test_to_dataframe_type(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=5, S0=100, T=1.0)
        df = gbm.to_dataframe()
        assert isinstance(df, pd.DataFrame)


class TestGBMStatistics:
    
    def test_get_statistics_keys(self):
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=100, S0=100, T=1.0)
        stats = gbm.get_statistics()
        
        expected_keys = {
            "mean_final_price",
            "std_final_price",
            "min_final_price",
            "max_final_price",
            "median_final_price",
            "mean_return",
            "std_return"
        }
        assert set(stats.keys()) == expected_keys
    
    def test_statistics_values_reasonable(self):
        np.random.seed(42)
        gbm = GBM(mu=0.08, sigma=0.2, n_steps=100, n_paths=1000, S0=100, T=1.0)
        stats = gbm.get_statistics()
        
        assert stats["mean_final_price"] > 100
        assert stats["std_final_price"] > 0
        assert stats["min_final_price"] < stats["mean_final_price"]
        assert stats["max_final_price"] > stats["mean_final_price"]
        assert stats["median_final_price"] > 0
    
    def test_zero_volatility_statistics(self):
        gbm = GBM(mu=0.05, sigma=0.0, n_steps=100, n_paths=10, S0=100, T=1.0)
        stats = gbm.get_statistics()
        
        expected_price = 100 * np.exp(0.05 * 1.0)
        assert abs(stats["mean_final_price"] - expected_price) < 0.01
        assert stats["std_final_price"] < 0.01
        assert abs(stats["min_final_price"] - expected_price) < 0.01
        assert abs(stats["max_final_price"] - expected_price) < 0.01
