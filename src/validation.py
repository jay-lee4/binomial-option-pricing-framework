
from typing import Tuple, Optional


def validate_strike_prices(K1: float, K2: float, K3: float, K4: float, S: float, strategy: str) -> Tuple[bool, Optional[str]]:
    """
    Validate strike price configuration.
    
    Args:
        K1, K2, K3, K4: Strike prices
        S: Current stock price
        strategy: Strategy type
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if strategy == "Iron Condor":
        # Iron Condor requires K1 < K2 < K3 < K4
        if not (K1 < K2 < K3 < K4):
            return False, "Iron Condor requires K1 < K2 < K3 < K4"
        
        # K2 should be below current price
        if K2 >= S:
            return False, "K2 (short put) should be below current stock price"
        
        # K3 should be above current price
        if K3 <= S:
            return False, "K3 (short call) should be above current stock price"
        
        # Check for reasonable spreads
        if K2 - K1 < 1:
            return False, "Spread between K1 and K2 is too narrow (minimum $1)"
        
        if K4 - K3 < 1:
            return False, "Spread between K3 and K4 is too narrow (minimum $1)"
        
        # Warn if strikes are too close to current price
        if abs(K2 - S) < S * 0.02:
            return False, "K2 is too close to current price (minimum 2% away)"
        
        if abs(K3 - S) < S * 0.02:
            return False, "K3 is too close to current price (minimum 2% away)"
    
    elif strategy == "Straddle":
        # K1 should be reasonably close to S
        if abs(K1 - S) > S * 0.5:
            return False, "Strike price is too far from current price (maximum 50%)"
    
    elif strategy == "Strangle":
        # K1 should be below S, K2 should be above S
        if K1 >= S:
            return False, "K1 (put strike) should be below current price"
        
        if K2 <= S:
            return False, "K2 (call strike) should be above current price"
        
        if K1 >= K2:
            return False, "K1 must be less than K2"
    
    return True, None


def validate_market_parameters(r: float, mu: float, sigma: float, T: float) -> Tuple[bool, Optional[str]]:
    """
    Validate market parameters.
    
    Args:
        r: Risk-free rate
        mu: Expected return
        sigma: Volatility
        T: Time to expiration
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Risk-free rate checks
    if r < 0:
        return False, "Risk-free rate cannot be negative"
    
    if r > 0.20:
        return False, "Risk-free rate seems too high (> 20%)"
    
    # Expected return checks
    if mu < -0.50:
        return False, "Expected return seems too negative (< -50%)"
    
    if mu > 0.50:
        return False, "Expected return seems too high (> 50%)"
    
    # Volatility checks
    if sigma <= 0:
        return False, "Volatility must be positive"
    
    if sigma < 0.01:
        return False, "Volatility is too low (< 1%)"
    
    if sigma > 2.0:
        return False, "Volatility seems too high (> 200%)"
    
    # Time to expiration checks
    if T <= 0:
        return False, "Time to expiration must be positive"
    
    if T > 5:
        return False, "Time to expiration is too long (> 5 years)"
    
    if T < 0.01:
        return False, "Time to expiration is too short (< 4 days)"
    
    return True, None


def validate_simulation_parameters(N: int, n_paths: int) -> Tuple[bool, Optional[str]]:
    """
    Validate simulation parameters.
    
    Args:
        N: Number of binomial steps
        n_paths: Number of Monte Carlo paths
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Binomial steps
    if N < 10:
        return False, "Number of binomial steps is too low (minimum 10)"
    
    if N > 10000:
        return False, "Number of binomial steps is too high (maximum 10,000)"
    
    # Monte Carlo paths
    if n_paths < 100:
        return False, "Number of Monte Carlo paths is too low (minimum 100)"
    
    if n_paths > 100000:
        return False, "Number of Monte Carlo paths is too high (maximum 100,000)"
    
    return True, None


def validate_stock_price(S: float) -> Tuple[bool, Optional[str]]:
    """
    Validate stock price.
    
    Args:
        S: Stock price
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if S <= 0:
        return False, "Stock price must be positive"
    
    if S < 1:
        return False, "Stock price seems too low (< $1)"
    
    if S > 100000:
        return False, "Stock price seems too high (> $100,000)"
    
    return True, None


def validate_all_inputs(inputs: dict) -> Tuple[bool, Optional[str]]:
    """
    Validate all inputs at once.
    
    Args:
        inputs: Dictionary of all user inputs
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate stock price
    is_valid, error = validate_stock_price(inputs['S'])
    if not is_valid:
        return False, f"Stock Price Error: {error}"
    
    # Validate strike prices
    is_valid, error = validate_strike_prices(
        inputs['K1'], inputs['K2'], inputs['K3'], inputs['K4'],
        inputs['S'], inputs['strategy']
    )
    if not is_valid:
        return False, f"Strike Price Error: {error}"
    
    # Validate market parameters
    is_valid, error = validate_market_parameters(
        inputs['r'], inputs['mu'], inputs['sigma'], inputs['T']
    )
    if not is_valid:
        return False, f"Market Parameter Error: {error}"
    
    # Validate simulation parameters
    is_valid, error = validate_simulation_parameters(
        inputs['N'], inputs['n_paths']
    )
    if not is_valid:
        return False, f"Simulation Parameter Error: {error}"
    
    return True, None
