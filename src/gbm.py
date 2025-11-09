import numpy as np


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
        """
        Generate all price paths using GBM.
        
        Returns:
            Array of shape (n_paths, n_steps+1) with simulated prices
        """
        random_normals = np.random.randn(self.n_paths, self.n_steps)
        dW = random_normals * np.sqrt(self.dt)
        
        # Log price increments
        dS = (self.mu - 0.5 * self.sigma ** 2) * self.dt + self.sigma * dW
        
        # Prepend zero for initial log price
        dS = np.column_stack([np.zeros(self.n_paths), dS])
        
        # Cumulative sum to get log prices, then exponentiate
        log_prices = np.cumsum(dS, axis=1)
        self.paths = self.S0 * np.exp(log_prices)
        
        return self.paths
    
    def get_final_prices(self) -> np.ndarray:
        """
        Get final prices from all paths.
        
        Returns:
            Array of shape (n_paths,) with terminal prices
        """
        if self.paths is None:
            self.get_all_paths()
        
        return self.paths[:, -1]
