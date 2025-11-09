import numpy as np


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
    dt = T / N
    
    # Tree parameters
    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp(-sigma * np.sqrt(dt))
    pu = (np.exp(r * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-r * dt)
    
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
