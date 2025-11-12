import numpy as np
from abc import ABC, abstractmethod
from .utils import n_choose, prob_profit
from .payouts import IronCondorPayout, StraddlePayout, StranglePayout


def exp_profits(
    S: float,
    n: int,
    u_star: float,
    d_start: float,
    p: float,
    K1: float,
    K2: float,
    K3: float,
    K4: float,
    initial_capital: float,
    payout_name: str = "iron_condor"
) -> float:
    """
    Calculate expected profit under real-world probability measure.
    
    Args:
        S: Current stock price
        n: Number of time steps
        u_star: Up factor
        d_start: Down factor
        p: Real-world probability of up move
        K1-K4: Strike prices
        initial_capital: Premium collected from selling strategy
        payout_name: Strategy type ('iron_condor', 'straddle', 'strangle')
        
    Returns:
        Expected profit = initial_capital - expected_payout
    """
    q = 1 - p
    range_ = np.arange(n + 1)
    
    # Terminal stock prices: S * u^(n-j) * d^j for j in [0, n]
    prices = S * (u_star ** (n - range_)) * (d_start ** range_)

    # Binomial probability: P(j down moves) = C(n,j) * p^(n-j) * q^j
    probs = (p ** (n - range_)) * (q ** range_)
    freq_list = n_choose(n) * probs
    
    if payout_name == "iron_condor":
        payout = IronCondorPayout(K1, K2, K3, K4)
    elif payout_name == "straddle":
        payout = StraddlePayout(K1)
    elif payout_name == "strangle":
        payout = StranglePayout(K1, K2)
    else:
        payout = IronCondorPayout(K1, K2, K3, K4)
    
    payout_values = payout.calculate_payout(prices)
    final_profit = initial_capital - payout_values
    expected_value = final_profit * freq_list
    
    return np.sum(expected_value)


class RWProbs(ABC):
    """
    Base class for real-world probability analysis.
    
    Calculates expected profits and probability of profit under
    real-world (P-measure) dynamics, not risk-neutral (Q-measure).
    """
    
    def __init__(
        self,
        model: str,
        S: float,
        m: float,
        r: float,
        sigma: float,
        T: float,
        N: int,
        K1: float,
        K2: float,
        K3: float,
        K4: float
    ):
        self.model = model
        self.S = S
        self.m = m  # Real-world drift (mu)
        self.r = r
        self.sigma = sigma
        self.T = T
        self.N = N
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.K4 = K4
        
        # Subclasses must set u_star and d_start
        self.u_star = None
        self.d_start = None
        
        # Real-world probability (from utils.calculate_p)
        from .utils import calculate_p
        self.p = calculate_p(m, r, sigma, T, N)
        self.q = 1 - self.p
    
    @abstractmethod
    def get_prob_profit(self) -> float:
        """Calculate probability of profit under real-world measure."""
        pass
    
    def get_exp_profits(self, initial_capital: float, payout_name: str = "iron_condor") -> float:
        return exp_profits(
            self.S, self.N, self.u_star, self.d_start,
            self.p, self.K1, self.K2, self.K3, self.K4,
            initial_capital, payout_name
        )
    
    @abstractmethod
    def get_probs(self) -> np.ndarray:
        """Get probability distribution over final states."""
        pass


class CoxRossRubinsteinRW(RWProbs):
    """Real-world probability analysis using CRR tree parameters."""
    
    def __init__(
        self,
        S: float,
        m: float,
        r: float,
        sigma: float,
        T: float,
        N: int,
        K1: float,
        K2: float,
        K3: float,
        K4: float
    ):
        super().__init__("Cox-Ross-Rubinstein", S, m, r, sigma, T, N, K1, K2, K3, K4)
        
        self.u_star = np.exp(self.sigma * np.sqrt(self.T / self.N))
        self.d_start = 1 / self.u_star
    
    def get_prob_profit(self) -> float:
        """Calculate probability of profit for Iron Condor."""
        return prob_profit(
            self.S, self.N, self.u_star, self.d_start,
            self.p, self.K1, self.K2, self.K3, self.K4
        )
    
    def get_probs(self) -> np.ndarray:
        """Get probability distribution over final states."""
        range_ = np.arange(self.N + 1)
        probs = (self.p ** (self.N - range_)) * (self.q ** range_)
        return probs


class SteveShreveRW(RWProbs):
    """Real-world probability analysis using Steve Shreve tree parameters."""
    
    def __init__(
        self,
        S: float,
        m: float,
        r: float,
        sigma: float,
        T: float,
        N: int,
        K1: float,
        K2: float,
        K3: float,
        K4: float
    ):
        super().__init__("Steve Shreve", S, m, r, sigma, T, N, K1, K2, K3, K4)
        
        temp = self.sigma * np.sqrt(self.T / self.N)
        temp2 = 1 + self.r * (self.T / self.N)
        self.u_star = temp2 + temp
        self.d_start = temp2 - temp
    
    def get_prob_profit(self) -> float:
        """Calculate probability of profit for Iron Condor."""
        return prob_profit(
            self.S, self.N, self.u_star, self.d_start,
            self.p, self.K1, self.K2, self.K3, self.K4
        )
    
    def get_probs(self) -> np.ndarray:
        """Get probability distribution over final states."""
        range_ = np.arange(self.N + 1)
        probs = (self.p ** (self.N - range_)) * (self.q ** range_)
        return probs


class DriftAdjustedRW(RWProbs):
    """Real-world probability analysis using drift-adjusted tree parameters."""
    
    def __init__(
        self,
        S: float,
        m: float,
        r: float,
        sigma: float,
        T: float,
        N: int,
        K1: float,
        K2: float,
        K3: float,
        K4: float
    ):
        super().__init__("Drift-Adjusted", S, m, r, sigma, T, N, K1, K2, K3, K4)
        
        temp = self.sigma * np.sqrt(self.T / self.N)
        temp2 = 1 + self.m * (self.T / self.N)
        self.u_star = temp2 + temp
        self.d_start = temp2 - temp
    
    def get_prob_profit(self) -> float:
        """Calculate probability of profit for Iron Condor."""
        return prob_profit(
            self.S, self.N, self.u_star, self.d_start,
            self.p, self.K1, self.K2, self.K3, self.K4
        )
    
    def get_probs(self) -> np.ndarray:
        """Get probability distribution over final states."""
        range_ = np.arange(self.N + 1)
        probs = (self.p ** (self.N - range_)) * (self.q ** range_)
        return probs
