import numpy as np
from scipy.special import comb
import math


def n_choose_k(n: int, k: int) -> int:
    """
    Calculate nCk (n choose k) - binomial coefficient.
    
    Args:
        n: Total number of items
        k: Number of items to choose
        
    Returns:
        Number of ways to choose k items from n items
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    if k > n // 2:
        k = n - k
        return math.comb(n, k)


def n_choose(n: int) -> np.ndarray:
    """
    Compute binomial coefficients nCk for all k in [0, n].
    
    This vectorized version returns an array of all binomial coefficients
    for a given n, which is used in probability calculations for binomial trees.
    
    Args:
        n: Number of time steps in binomial tree
        
    Returns:
        Array of shape (n+1,) containing [nC0, nC1, ..., nCn]
    """
    return comb(n, np.arange(n + 1), exact=False)


def calculate_p(m: float, r: float, sigma: float, T: float, N: int) -> float:
    """
    Calculate the real-world probability of an upward price move.
    
    This probability (p) is used in the real-world (P-measure) analysis
    to calculate expected profits under actual market dynamics, not the
    risk-neutral measure.
    
    Formula: p = 0.5 - ((r - m) * (T/N)) / (2 * sigma * sqrt(T/N))
    
    Args:
        m: Expected return (mu/drift) of the underlying asset
        r: Risk-free interest rate
        sigma: Volatility of the underlying asset
        T: Time to maturity in years
        N: Number of time steps in binomial tree
        
    Returns:
        Probability of upward move (between 0 and 1)
    """
    dt = T / N
    numerator = (r - m) * dt
    denominator = 2 * sigma * np.sqrt(dt)
    
    return 0.5 - (numerator / denominator)


def prob_profit(
    S: float,
    n: int,
    u_star: float,
    d_start: float,
    p: float,
    K1: float,
    K2: float,
    K3: float,
    K4: float
) -> float:
    """
    Calculate the probability of profit for an Iron Condor strategy.
    
    The strategy is profitable when the final stock price lands between
    the average of K1-K2 (lower bound) and K3-K4 (upper bound).
    
    Args:
        S: Current stock price
        n: Number of time steps
        u_star: Up factor in binomial tree
        d_start: Down factor in binomial tree
        p: Real-world probability of up move
        K1: Strike of long put (lowest)
        K2: Strike of short put
        K3: Strike of short call
        K4: Strike of long call (highest)
        
    Returns:
        Probability of profit (between 0 and 1)
        
    Note:
        Profit zone is defined as: (K1+K2)/2 < S_T < (K3+K4)/2
    """
    q = 1 - p
    range_ = np.arange(n + 1)
    
    # Calculate possible final prices
    prices = S * (u_star ** (n - range_)) * (d_start ** range_)
    
    # Define profit boundaries
    lower_bound = (K2 + K1) / 2
    upper_bound = (K3 + K4) / 2
    
    # Create mask for profitable price range
    lower_mask = prices > lower_bound
    upper_mask = prices < upper_bound
    mask = np.logical_and(lower_mask, upper_mask)
    
    # Calculate probability for each outcome
    probs = (p ** (n - range_)) * (q ** range_)
    freq_list = n_choose(n) * probs
    
    return np.sum(freq_list[mask])
