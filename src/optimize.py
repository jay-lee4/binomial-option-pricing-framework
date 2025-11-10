"""Strike price optimization logic."""

import numpy as np
from tqdm import tqdm
from .models import cox_ross_rubinstein, steve_shreve, drift_adjusted
from .payouts import IronCondorPayout, StraddlePayout, StranglePayout
from .analytics import CoxRossRubinsteinRW, SteveShreveRW, DriftAdjustedRW


def calculate_initial_capitals(S, K1, K2, K3, K4, T, r, sigma, mu, N):
    """
    Calculate initial capital for all three models.
    
    Args:
        S: Current stock price
        K1, K2, K3, K4: Strike prices
        T: Time to expiration
        r: Risk-free rate
        sigma: Volatility
        mu: Expected return
        N: Number of time steps
        
    Returns:
        Dictionary with initial capital for each model
    """
    prices = {
        'CRR': {},
        'Steve Shreve': {},
        'Drift-Adjusted': {}
    }
    
    # Price all four strikes
    for strike, strike_name in [(K1, 'K1'), (K2, 'K2'), (K3, 'K3'), (K4, 'K4')]:
        # K1 and K2 are puts, K3 and K4 are calls
        option_type = 'P' if strike_name in ['K1', 'K2'] else 'C'
        
        prices['CRR'][strike_name] = cox_ross_rubinstein(S, strike, T, r, sigma, N, option_type)
        prices['Steve Shreve'][strike_name] = steve_shreve(S, strike, T, r, sigma, N, option_type)
        prices['Drift-Adjusted'][strike_name] = drift_adjusted(S, strike, T, r, sigma, mu, N, option_type)
    
    # Calculate initial capital (Iron Condor: sell K2 put + sell K3 call - buy K1 put - buy K4 call)
    initial_capitals = {
        'CRR': prices['CRR']['K2'] + prices['CRR']['K3'] - prices['CRR']['K1'] - prices['CRR']['K4'],
        'Steve Shreve': prices['Steve Shreve']['K2'] + prices['Steve Shreve']['K3'] - 
                        prices['Steve Shreve']['K1'] - prices['Steve Shreve']['K4'],
        'Drift-Adjusted': prices['Drift-Adjusted']['K2'] + prices['Drift-Adjusted']['K3'] - 
                          prices['Drift-Adjusted']['K1'] - prices['Drift-Adjusted']['K4']
    }
    
    return initial_capitals


def strike_to_profit_gbm(K1, K2, K3, K4, final_prices, initial_capital, payout_name='iron_condor'):
    """
    Calculate expected profit from GBM simulation.
    
    Args:
        K1, K2, K3, K4: Strike prices
        final_prices: Array of simulated final prices
        initial_capital: Premium collected
        payout_name: Strategy type
        
    Returns:
        Expected profit
    """
    if payout_name == 'iron_condor':
        payout = IronCondorPayout(K1, K2, K3, K4)
    elif payout_name == 'straddle':
        payout = StraddlePayout(K1)
    elif payout_name == 'strangle':
        payout = StranglePayout(K1, K2)
    else:
        payout = IronCondorPayout(K1, K2, K3, K4)
    
    payout_values = payout.calculate_payout(final_prices)
    average_payout = np.mean(payout_values)
    
    return initial_capital - average_payout


def generate_strike_grid(S, grid_size='medium'):
    """
    Generate grid of strike price combinations to test.
    
    Args:
        S: Current stock price
        grid_size: 'small', 'medium', or 'large'
        
    Returns:
        List of (K1, K2, K3, K4) tuples
    """
    if grid_size == 'small':
        step = 10
        k1_range = range(int(S * 0.7), int(S * 0.95), step)
        k2_range_offset = [5, 10]
        k3_range_offset = [5, 10]
        k4_range_offset = [5, 10]
    elif grid_size == 'large':
        step = 5
        k1_range = range(int(S * 0.6), int(S * 0.95), step)
        k2_range_offset = list(range(5, 20, 5))
        k3_range_offset = list(range(5, 20, 5))
        k4_range_offset = list(range(5, 20, 5))
    else:  # medium
        step = 10
        k1_range = range(int(S * 0.7), int(S * 0.95), step)
        k2_range_offset = [5, 10, 15]
        k3_range_offset = [5, 10, 15]
        k4_range_offset = [5, 10, 15]
    
    strike_combinations = []
    
    for k1 in k1_range:
        for k2_offset in k2_range_offset:
            k2 = k1 + k2_offset
            if k2 >= S:
                continue
            
            for k3_offset in k3_range_offset:
                k3 = int(S) + k3_offset
                
                for k4_offset in k4_range_offset:
                    k4 = k3 + k4_offset
                    
                    # Ensure valid ordering
                    if k1 < k2 < k3 < k4:
                        strike_combinations.append((k1, k2, k3, k4))
    
    return strike_combinations


def optimize_strikes(S, r, T, sigma, mu, final_prices, N=1000, grid_size='medium', payout_name='iron_condor'):
    """
    Find optimal strike prices for maximizing expected profit.
    
    Args:
        S: Current stock price
        r: Risk-free rate
        T: Time to expiration
        sigma: Volatility
        mu: Expected return
        final_prices: Array of simulated final prices from GBM
        N: Number of binomial steps
        grid_size: 'small', 'medium', or 'large'
        payout_name: Strategy type
        
    Returns:
        Dictionary with optimal strikes and expected profits for each model
    """
    strike_combinations = generate_strike_grid(S, grid_size)
    
    results = {
        'CRR': {
            'GBM_optimal_strikes': None,
            'GBM_max_profit': -np.inf,
            'RW_optimal_strikes': None,
            'RW_max_profit': -np.inf,
            'RW_prob_profit': None
        },
        'Steve Shreve': {
            'GBM_optimal_strikes': None,
            'GBM_max_profit': -np.inf,
            'RW_optimal_strikes': None,
            'RW_max_profit': -np.inf,
            'RW_prob_profit': None
        },
        'Drift-Adjusted': {
            'GBM_optimal_strikes': None,
            'GBM_max_profit': -np.inf,
            'RW_optimal_strikes': None,
            'RW_max_profit': -np.inf,
            'RW_prob_profit': None
        }
    }
    
    # Test all strike combinations
    for k1, k2, k3, k4 in tqdm(strike_combinations, desc="Optimizing strikes"):
        try:
            # Calculate initial capitals for this strike combination
            initial_capitals = calculate_initial_capitals(S, k1, k2, k3, k4, T, r, sigma, mu, N)
            
            # For each model
            for model_name in ['CRR', 'Steve Shreve', 'Drift-Adjusted']:
                # Calculate GBM expected profit
                gbm_profit = strike_to_profit_gbm(
                    k1, k2, k3, k4, 
                    final_prices, 
                    initial_capitals[model_name],
                    payout_name
                )
                
                # Update if better than current best
                if gbm_profit > results[model_name]['GBM_max_profit']:
                    results[model_name]['GBM_max_profit'] = gbm_profit
                    results[model_name]['GBM_optimal_strikes'] = (k1, k2, k3, k4)
                
                # Calculate RW expected profit
                if model_name == 'CRR':
                    rw = CoxRossRubinsteinRW(S, mu, r, sigma, T, N, k1, k2, k3, k4)
                elif model_name == 'Steve Shreve':
                    rw = SteveShreveRW(S, mu, r, sigma, T, N, k1, k2, k3, k4)
                else:
                    rw = DriftAdjustedRW(S, mu, r, sigma, T, N, k1, k2, k3, k4)
                
                rw_profit = rw.get_exp_profits(initial_capitals[model_name], payout_name)
                
                # Update if better than current best
                if rw_profit > results[model_name]['RW_max_profit']:
                    results[model_name]['RW_max_profit'] = rw_profit
                    results[model_name]['RW_optimal_strikes'] = (k1, k2, k3, k4)
                    results[model_name]['RW_prob_profit'] = rw.get_prob_profit()
        
        except Exception as e:
            # Skip invalid combinations
            continue
    
    return results
