import numpy as np
import pandas as pd


class GBM:
    """
    Geometric Brownian Motion simulator.
    
    Models stock price evolution: dS/S = μ*dt + σ*dW_t
    
    where:
    - μ (mu): drift/expected return
    - σ (sigma): volatility
    - dW_t: Wiener process increment
    """
    
    def __init__(
        self,
        mu: float,
        sigma: float,
        n_steps: int,
        n_paths: int,
        S0: float,
        T: float
    ):
        """
        Initialize GBM simulator.
        
        Args:
            mu: Drift (expected return)
            sigma: Volatility
            n_steps: Number of time steps
            n_paths: Number of simulation paths
            S0: Initial stock price
            T: Time horizon (years)
        """
        
        if S0 <= 0:
            raise ValueError(f"Initial stock price must be positive, got {S0}")
        if sigma < 0:
            raise ValueError(f"Volatility must be non-negative, got {sigma}")
        if n_steps <= 0:
            raise ValueError(f"Number of steps must be positive, got {n_steps}")
        if n_paths <= 0:
            raise ValueError(f"Number of paths must be positive, got {n_paths}")
        if T <= 0:
            raise ValueError(f"Time horizon must be positive, got {T}")
        
        self.mu = mu
        self.sigma = sigma
        self.n_steps = n_steps
        self.n_paths = n_paths
        self.S0 = S0
        self.T = T
        self.dt = T / n_steps
        self.paths = None
    
    def get_all_paths(self) -> np.ndarray:
        random_normals = np.random.randn(self.n_paths, self.n_steps)
        dW = random_normals * np.sqrt(self.dt)
        
        # Ito's lemma drift correction: (μ - σ²/2) accounts for 
        # quadratic variation in continuous-time limit
        dS = (self.mu - 0.5 * self.sigma ** 2) * self.dt + self.sigma * dW
        
        dS = np.column_stack([np.zeros(self.n_paths), dS])
        
        log_prices = np.cumsum(dS, axis=1)
        self.paths = self.S0 * np.exp(log_prices)
        
        return self.paths
    
    def get_final_prices(self) -> np.ndarray:
        if self.paths is None:
            self.get_all_paths()
        
        return self.paths[:, -1]
    
    def to_dataframe(self) -> pd.DataFrame:
        if self.paths is None:
            self.get_all_paths()
        
        time_steps = np.linspace(0, self.T, self.n_steps + 1)
        
        df = pd.DataFrame(
            self.paths.T,
            index=time_steps,
            columns=[f"Path_{i+1}" for i in range(self.n_paths)]
        )
        df.index.name = "Time"
        
        return df
    
    def get_statistics(self) -> dict:
        if self.paths is None:
            self.get_all_paths()
        
        final_prices = self.get_final_prices()
        
        return {
            "mean_final_price": np.mean(final_prices),
            "std_final_price": np.std(final_prices),
            "min_final_price": np.min(final_prices),
            "max_final_price": np.max(final_prices),
            "median_final_price": np.median(final_prices),
            "mean_return": np.mean(final_prices / self.S0 - 1),
            "std_return": np.std(final_prices / self.S0 - 1)
        }
