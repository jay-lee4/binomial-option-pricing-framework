import pandas as pd
import json
from datetime import datetime


def export_results_to_csv(results, inputs):
    """
    Export calculation results to CSV format.
    
    Args:
        results: Dictionary containing calculation results
        inputs: Dictionary of user inputs
        
    Returns:
        DataFrame ready for CSV export
    """
    models = ['CRR', 'Steve Shreve', 'Drift-Adjusted']
    
    data = []
    for model in models:
        row = {
            'Model': model,
            'K1_Price': results[model].get('K1', 0),
            'K2_Price': results[model].get('K2', 0),
            'K3_Price': results[model].get('K3', 0),
            'K4_Price': results[model].get('K4', 0),
            'Initial_Capital': results[model]['Initial Capital'],
            'GBM_Expected_Profit': results[model]['GBM Expected Value'],
            'RW_Expected_Profit': results[model]['RW Expected Value'],
            'Probability_of_Profit': results[model].get('Probability of Profit', 'N/A')
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df


def export_parameters_to_json(inputs):
    """
    Export parameters to JSON format.
    
    Args:
        inputs: Dictionary of user inputs
        
    Returns:
        JSON string of parameters
    """
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'parameters': {
            'strategy': inputs['strategy'],
            'stock_price': float(inputs['S']),
            'strike_prices': {
                'K1': float(inputs['K1']),
                'K2': float(inputs['K2']),
                'K3': float(inputs['K3']),
                'K4': float(inputs['K4'])
            },
            'market_parameters': {
                'risk_free_rate': float(inputs['r']),
                'expected_return': float(inputs['mu']),
                'volatility': float(inputs['sigma']),
                'time_to_expiry': float(inputs['T'])
            },
            'simulation_parameters': {
                'binomial_steps': int(inputs['N']),
                'monte_carlo_paths': int(inputs['n_paths'])
            }
        }
    }
    
    return json.dumps(export_data, indent=2)


def export_optimization_to_csv(opt_results):
    """
    Export optimization results to CSV format.
    
    Args:
        opt_results: Dictionary containing optimization results
        
    Returns:
        DataFrame ready for CSV export
    """
    models = ['CRR', 'Steve Shreve', 'Drift-Adjusted']
    
    data = []
    for model in models:
        # GBM optimal
        gbm_k1, gbm_k2, gbm_k3, gbm_k4 = opt_results[model]['GBM_optimal_strikes']
        # RW optimal
        rw_k1, rw_k2, rw_k3, rw_k4 = opt_results[model]['RW_optimal_strikes']
        
        row = {
            'Model': model,
            'GBM_K1': gbm_k1,
            'GBM_K2': gbm_k2,
            'GBM_K3': gbm_k3,
            'GBM_K4': gbm_k4,
            'GBM_Max_Profit': opt_results[model]['GBM_max_profit'],
            'RW_K1': rw_k1,
            'RW_K2': rw_k2,
            'RW_K3': rw_k3,
            'RW_K4': rw_k4,
            'RW_Max_Profit': opt_results[model]['RW_max_profit'],
            'RW_Prob_Profit': opt_results[model].get('RW_prob_profit', 'N/A')
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df


def export_simulation_data_to_csv(simulation_data):
    """
    Export GBM simulation data to CSV format.
    
    Args:
        simulation_data: Dictionary containing simulation results
        
    Returns:
        DataFrame ready for CSV export
    """
    final_prices = simulation_data['final_prices']
    payout_values = simulation_data['payout_values']
    
    df = pd.DataFrame({
        'Final_Price': final_prices,
        'Payout': payout_values,
        'Profit_Loss': -payout_values
    })
    
    return df


def create_full_export_package(results, inputs, opt_results=None):
    """
    Create a complete export package with all data.
    
    Args:
        results: Calculation results
        inputs: User inputs
        opt_results: Optimization results (optional)
        
    Returns:
        Dictionary of DataFrames for each export type
    """
    package = {
        'results': export_results_to_csv(results, inputs),
        'parameters': export_parameters_to_json(inputs),
        'simulation': export_simulation_data_to_csv(results['simulation'])
    }
    
    if opt_results:
        package['optimization'] = export_optimization_to_csv(opt_results)
    
    return package
