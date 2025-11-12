from typing import Tuple, Optional

from .constants import (
    # Strike validation
    MIN_STRIKE_SEPARATION_PCT,
    MIN_SPREAD_WIDTH,
    # Volatility
    MIN_VOLATILITY,
    MAX_VOLATILITY,
    # Time
    MIN_TIME_TO_EXPIRY,
    MAX_TIME_TO_EXPIRY,
    # Rates
    MIN_RISK_FREE_RATE,
    MAX_RISK_FREE_RATE,
    MIN_EXPECTED_RETURN,
    MAX_EXPECTED_RETURN,
    # Stock price
    MIN_STOCK_PRICE,
    MAX_STOCK_PRICE,
    # Simulation parameters
    MIN_BINOMIAL_STEPS,
    MAX_BINOMIAL_STEPS,
    MIN_MC_PATHS,
    MAX_MC_PATHS,
)


def validate_strike_prices(
    K1: float, K2: float, K3: float, K4: float, S: float, strategy: str
) -> Tuple[bool, Optional[str]]:
    """
    Validate strike price configuration for a given strategy.
    
    Args:
        K1, K2, K3, K4: Strike prices
        S: Current stock price
        strategy: Strategy type ('Iron Condor', 'Straddle', or 'Strangle')
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if strikes are valid, False otherwise
        - error_message: None if valid, descriptive error string if invalid
    """
    if strategy == "Iron Condor":
        # Ordering constraint
        if not (K1 < K2 < K3 < K4):
            return False, "Iron Condor requires K1 < K2 < K3 < K4"
        
        # K2 must be below current price (short put)
        if K2 >= S:
            return False, "K2 (short put) should be below current stock price"
        
        # K3 must be above current price (short call)
        if K3 <= S:
            return False, "K3 (short call) should be above current stock price"
        
        # Check spread widths
        if K2 - K1 < MIN_SPREAD_WIDTH:
            return False, (
                f"Spread between K1 and K2 is too narrow "
                f"(minimum ${MIN_SPREAD_WIDTH:.2f})"
            )
        
        if K4 - K3 < MIN_SPREAD_WIDTH:
            return False, (
                f"Spread between K3 and K4 is too narrow "
                f"(minimum ${MIN_SPREAD_WIDTH:.2f})"
            )
        
        # Check separation from current price
        if abs(K2 - S) < S * MIN_STRIKE_SEPARATION_PCT:
            return False, (
                f"K2 is too close to current price "
                f"(minimum {MIN_STRIKE_SEPARATION_PCT*100:.0f}% away)"
            )
        
        if abs(K3 - S) < S * MIN_STRIKE_SEPARATION_PCT:
            return False, (
                f"K3 is too close to current price "
                f"(minimum {MIN_STRIKE_SEPARATION_PCT*100:.0f}% away)"
            )
    
    elif strategy == "Straddle":
        # Strike should be reasonably close to current price
        max_deviation_pct = 0.50  # Allow up to 50% deviation for straddles
        if abs(K1 - S) > S * max_deviation_pct:
            return False, (
                f"Strike price is too far from current price "
                f"(maximum {max_deviation_pct*100:.0f}%)"
            )
    
    elif strategy == "Strangle":
        # K1 (put) should be below S
        if K1 >= S:
            return False, "K1 (put strike) should be below current price"
        
        # K2 (call) should be above S
        if K2 <= S:
            return False, "K2 (call strike) should be above current price"
        
        # K1 must be less than K2
        if K1 >= K2:
            return False, "K1 must be less than K2"
    
    return True, None


def validate_market_parameters(
    r: float, mu: float, sigma: float, T: float
) -> Tuple[bool, Optional[str]]:
    """
    Validate market parameters for option pricing.
    
    Args:
        r: Risk-free rate (annualized)
        mu: Expected return (annualized)
        sigma: Volatility (annualized)
        T: Time to expiration (years)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Risk-free rate checks
    if r < MIN_RISK_FREE_RATE:
        return False, "Risk-free rate cannot be negative"
    
    if r > MAX_RISK_FREE_RATE:
        return False, (
            f"Risk-free rate seems too high (> {MAX_RISK_FREE_RATE*100:.0f}%)"
        )
    
    # Expected return checks
    if mu < MIN_EXPECTED_RETURN:
        return False, (
            f"Expected return seems too negative "
            f"(< {MIN_EXPECTED_RETURN*100:.0f}%)"
        )
    
    if mu > MAX_EXPECTED_RETURN:
        return False, (
            f"Expected return seems too high (> {MAX_EXPECTED_RETURN*100:.0f}%)"
        )
    
    # Volatility checks
    if sigma <= 0:
        return False, "Volatility must be positive"
    
    if sigma < MIN_VOLATILITY:
        return False, f"Volatility is too low (< {MIN_VOLATILITY*100:.0f}%)"
    
    if sigma > MAX_VOLATILITY:
        return False, f"Volatility seems too high (> {MAX_VOLATILITY*100:.0f}%)"
    
    # Time to expiration checks
    if T <= 0:
        return False, "Time to expiration must be positive"
    
    if T > MAX_TIME_TO_EXPIRY:
        return False, (
            f"Time to expiration is too long (> {MAX_TIME_TO_EXPIRY:.0f} years)"
        )
    
    if T < MIN_TIME_TO_EXPIRY:
        return False, (
            f"Time to expiration is too short "
            f"(< {MIN_TIME_TO_EXPIRY*365:.0f} days)"
        )
    
    return True, None


def validate_simulation_parameters(N: int, n_paths: int) -> Tuple[bool, Optional[str]]:
    """
    Validate simulation parameters for binomial trees and Monte Carlo.
    
    Args:
        N: Number of binomial tree steps
        n_paths: Number of Monte Carlo simulation paths
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Binomial steps validation
    if N < MIN_BINOMIAL_STEPS:
        return False, (
            f"Number of binomial steps is too low (minimum {MIN_BINOMIAL_STEPS})"
        )
    
    if N > MAX_BINOMIAL_STEPS:
        return False, (
            f"Number of binomial steps is too high "
            f"(maximum {MAX_BINOMIAL_STEPS:,})"
        )
    
    # Monte Carlo paths validation
    if n_paths < MIN_MC_PATHS:
        return False, (
            f"Number of Monte Carlo paths is too low (minimum {MIN_MC_PATHS})"
        )
    
    if n_paths > MAX_MC_PATHS:
        return False, (
            f"Number of Monte Carlo paths is too high "
            f"(maximum {MAX_MC_PATHS:,})"
        )
    
    return True, None


def validate_stock_price(S: float) -> Tuple[bool, Optional[str]]:
    """
    Validate current stock price.
    
    Args:
        S: Stock price
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if S <= 0:
        return False, "Stock price must be positive"
    
    if S < MIN_STOCK_PRICE:
        return False, f"Stock price seems too low (< ${MIN_STOCK_PRICE:.2f})"
    
    if S > MAX_STOCK_PRICE:
        return False, (
            f"Stock price seems too high (> ${MAX_STOCK_PRICE:,.0f})"
        )
    
    return True, None


def validate_all_inputs(inputs: dict) -> Tuple[bool, Optional[str]]:
    """
    Validate all inputs at once.
    
    Runs all validation checks in sequence and returns the first error found.
    
    Args:
        inputs: Dictionary of all user inputs containing:
            - S: stock price
            - K1, K2, K3, K4: strike prices
            - r: risk-free rate
            - mu: expected return
            - sigma: volatility
            - T: time to expiration
            - N: binomial steps
            - n_paths: Monte Carlo paths
            - strategy: strategy type
        
    Returns:
        Tuple of (is_valid, error_message)
        - Returns (True, None) if all validations pass
        - Returns (False, error_message) on first validation failure
    """
    # Validate stock price first (needed for strike validation)
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
