import numpy as np
from functools import lru_cache
from .constants import VALID_OPTION_TYPES, TREE_PARAMS_CACHE_SIZE


@lru_cache(maxsize=TREE_PARAMS_CACHE_SIZE)
def _get_crr_params(N: int, T: float, r: float, sigma: float) -> tuple:
    """
    Precompute CRR tree parameters (cached for reuse).
    
    Returns:
        (dt, u, d, pu, pd, disc)
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp(-sigma * np.sqrt(dt))
    pu = (np.exp(r * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-r * dt)
    return dt, u, d, pu, pd, disc


@lru_cache(maxsize=TREE_PARAMS_CACHE_SIZE)
def _get_shreve_params(N: int, T: float, r: float, sigma: float) -> tuple:
    """
    Precompute Steve Shreve tree parameters (cached for reuse).
    
    Returns:
        (dt, u, d, pu, pd, disc)
    """
    dt = T / N
    temp = sigma * np.sqrt(dt)
    temp2 = 1 + r * dt
    
    u = temp2 + temp
    d = temp2 - temp
    pu = 0.5
    pd = 0.5
    disc = np.exp(-r * dt)
    
    return dt, u, d, pu, pd, disc


@lru_cache(maxsize=TREE_PARAMS_CACHE_SIZE)
def _get_drift_params(N: int, T: float, r: float, sigma: float, mu: float) -> tuple:
    """
    Precompute drift-adjusted tree parameters (cached for reuse).
    
    Returns:
        (dt, u, d, pu, pd, disc)
    """
    dt = T / N
    temp = sigma * np.sqrt(dt)
    temp2 = 1 + mu * dt
    
    u = temp2 + temp
    d = temp2 - temp
    pu = (np.exp(r * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-r * dt)
    
    return dt, u, d, pu, pd, disc


def cox_ross_rubinstein(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    N: int,
    option_type: str
) -> float:
    """
    Price European option using Cox-Ross-Rubinstein binomial tree.
    
    Uses standard risk-neutral probabilities with:
    - u = exp(σ√Δt)
    - d = exp(-σ√Δt)
    - p = (exp(rΔt) - d) / (u - d)
    
    Args:
        S: Current stock price
        K: Strike price
        T: Time to maturity (years)
        r: Risk-free rate
        sigma: Volatility
        N: Number of time steps
        option_type: 'C' for call, 'P' for put
    
    Returns:
        Option price
    """
    if option_type not in VALID_OPTION_TYPES:
        raise ValueError(
            f"option_type must be 'C' or 'P', got '{option_type}'"
        )
    
    dt, u, d, pu, pd, disc = _get_crr_params(N, T, r, sigma)
    
    # Terminal stock prices at maturity
    S_0 = S * d**N
    ratio = u / d
    St = S_0 * ratio**np.arange(N + 1)
    
    # Terminal option values
    if option_type == 'C':
        C = np.maximum(St - K, 0)
    elif option_type == 'P':
        C = np.maximum(K - St, 0)
    else:
        raise ValueError(f"option_type must be 'C' or 'P', got '{option_type}'")
    
    # Backward induction
    for i in range(N, 0, -1):
        C[:i] = disc * (pu * C[1:i+1] + pd * C[:i])
    
    return C[0]


def steve_shreve(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    N: int,
    option_type: str
) -> float:
    """
    Price European option using Steve Shreve's linear approximation tree.
    
    Uses simplified factors:
    - u = 1 + r(T/N) + σ√(T/N)
    - d = 1 + r(T/N) - σ√(T/N)
    - p = 0.5 (symmetric construction)
    
    Args:
        S: Current stock price
        K: Strike price
        T: Time to maturity (years)
        r: Risk-free rate
        sigma: Volatility
        N: Number of time steps
        option_type: 'C' for call, 'P' for put
    
    Returns:
        Option price
        
    Raises:
        ValueError: If option_type not in {'C', 'P'}
    """
    if option_type not in VALID_OPTION_TYPES:
        raise ValueError(
            f"option_type must be 'C' or 'P', got '{option_type}'"
        )
    
    dt, u, d, pu, pd, disc = _get_shreve_params(N, T, r, sigma)
    
    # Vectorized calculation: S_0 * u^j * d^(N-j) for j=0 to N
    # Avoids explicit loop over all nodes at maturity
    S_terminal = S * d**N * (u/d)**np.arange(N + 1)
    
    # Terminal option values
    if option_type == 'C':
        option_values = np.maximum(S_terminal - K, 0)
    else:  # 'P'
        option_values = np.maximum(K - S_terminal, 0)
    
    # Backward induction
    for _ in range(N):
        option_values = disc * (pu * option_values[1:] + pd * option_values[:-1])
    
    return float(option_values[0])


def drift_adjusted(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    mu: float,
    N: int,
    option_type: str
) -> float:
    """
    Price European option using drift-adjusted binomial tree.
    
    Incorporates real-world drift (mu) in tree construction:
    - u = 1 + μ(T/N) + σ√(T/N)
    - d = 1 + μ(T/N) - σ√(T/N)
    - p = (exp(rΔt) - d) / (u - d) (risk-neutral for pricing)
    
    Note: While tree uses real-world drift, pricing still uses 
    risk-neutral probability to ensure no-arbitrage.
    
    Args:
        S: Current stock price
        K: Strike price
        T: Time to maturity (years)
        r: Risk-free rate
        sigma: Volatility
        mu: Expected return (drift)
        N: Number of time steps
        option_type: 'C' for call, 'P' for put
    
    Returns:
        Option price
        
    Raises:
        ValueError: If option_type not in {'C', 'P'}
    """
    if option_type not in VALID_OPTION_TYPES:
        raise ValueError(f"option_type must be 'C' or 'P', got '{option_type}'")
    
    dt, u, d, pu, pd, disc = _get_drift_params(N, T, r, sigma, mu)
    
    # Terminal stock prices - vectorized
    S_terminal = S * d**N * (u/d)**np.arange(N + 1)
    
    # Terminal option values
    if option_type == 'C':
        option_values = np.maximum(S_terminal - K, 0)
    else:  # 'P'
        option_values = np.maximum(K - S_terminal, 0)
    
    # Backward induction
    for _ in range(N):
        option_values = disc * (pu * option_values[1:] + pd * option_values[:-1])
    
    return float(option_values[0])
