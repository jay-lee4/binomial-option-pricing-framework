import streamlit as st
import numpy as np

# Config imports
from config.settings import DEFAULT_PARAMS

# Component imports
from components.sidebar import render_sidebar
from components.results_display import (
    display_pricing_results, 
    display_summary_metrics,
    display_q_vs_p_comparison,
    display_profitability_insight
)
from components.charts import (
    plot_gbm_paths, 
    plot_payout_diagram, 
    plot_price_distribution
)
from components.optimization_display import (
    display_optimization_button,
    display_optimization_results,
    display_optimization_summary_card,
    plot_optimal_comparison,
    display_improvement_metrics,
    display_apply_optimal_button
)

# Model imports
from src.models import cox_ross_rubinstein, steve_shreve, drift_adjusted
from src.gbm import GBM
from src.payouts import IronCondorPayout, StraddlePayout, StranglePayout
from src.analytics import CoxRossRubinsteinRW, SteveShreveRW, DriftAdjustedRW
from src.optimize import optimize_strikes


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Options Simulator",
        page_icon="chart_with_upwards_trend",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_custom_css():
    st.markdown("""
        <style>
        .main {
            padding: 1rem 2rem;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 600;
            color: #1e293b;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            color: #64748b;
            font-weight: 500;
        }
        
        h1 {
            font-weight: 700;
            color: #1e3a8a;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #3b82f6;
            margin-bottom: 1.5rem;
        }
        
        h2 {
            font-weight: 600;
            color: #1e40af;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            font-weight: 600;
            color: #374151;
            margin-top: 1.5rem;
        }
        
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transform: translateY(-1px);
        }
        
        /* Sidebar styling - dark background */
        [data-testid="stSidebar"] {
            background-color: #1e293b;
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #f1f5f9 !important;
        }
        
        /* Sidebar input fields */
        [data-testid="stSidebar"] .stNumberInput label,
        [data-testid="stSidebar"] .stSelectbox label {
            color: #e2e8f0 !important;
        }
        
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] select {
            background-color: #334155 !important;
            color: #f1f5f9 !important;
            border: 1px solid #475569 !important;
        }
        
        /* Sidebar expander */
        [data-testid="stSidebar"] .streamlit-expanderHeader {
            background-color: #334155;
            color: #f1f5f9 !important;
        }
        
        /* Sidebar divider */
        [data-testid="stSidebar"] hr {
            border-color: #475569;
        }
        
        [data-testid="stDataFrame"] {
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
        }
        
        .stAlert {
            border-radius: 0.5rem;
            border-left: 4px solid #3b82f6;
        }
        
        hr {
            margin: 2rem 0;
            border-color: #e2e8f0;
        }
        
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            border-radius: 0.375rem;
            border: 1px solid #cbd5e1;
            background-color: white;
            color: #1e293b;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1rem;
            font-weight: 600;
            color: #475569;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #eff6ff;
            border-bottom: 2px solid #3b82f6;
            color: #1e40af;
        }
        </style>
    """, unsafe_allow_html=True)


def calculate_prices(inputs):
    """
    Calculate option prices and expected values for all models.
    
    Args:
        inputs: Dictionary of user inputs from sidebar
        
    Returns:
        Dictionary containing pricing results and simulation data
    """
    S = inputs["S"]
    K1 = inputs["K1"]
    K2 = inputs["K2"]
    K3 = inputs["K3"]
    K4 = inputs["K4"]
    T = inputs["T"]
    r = inputs["r"]
    sigma = inputs["sigma"]
    mu = inputs["mu"]
    N = inputs["N"]
    n_paths = inputs["n_paths"]
    strategy = inputs["strategy"]
    
    payout_map = {
        "Iron Condor": "iron_condor",
        "Straddle": "straddle",
        "Strangle": "strangle"
    }
    payout_name = payout_map[strategy]
    
    results = {
        "CRR": {},
        "Steve Shreve": {},
        "Drift-Adjusted": {}
    }
    
    # Calculate option prices for each strike
    for strike, strike_name in [(K1, "K1"), (K2, "K2"), (K3, "K3"), (K4, "K4")]:
        if strategy == "Iron Condor":
            option_type = "P" if strike_name in ["K1", "K2"] else "C"
        elif strategy == "Straddle":
            option_type = "C"
        elif strategy == "Strangle":
            option_type = "P" if strike_name == "K1" else "C"
        
        results["CRR"][strike_name] = cox_ross_rubinstein(S, strike, T, r, sigma, N, option_type)
        results["Steve Shreve"][strike_name] = steve_shreve(S, strike, T, r, sigma, N, option_type)
        results["Drift-Adjusted"][strike_name] = drift_adjusted(S, strike, T, r, sigma, mu, N, option_type)
    
    # Calculate initial capital based on strategy
    if strategy == "Iron Condor":
        results["CRR"]["Initial Capital"] = (
            results["CRR"]["K2"] + results["CRR"]["K3"] - 
            results["CRR"]["K1"] - results["CRR"]["K4"]
        )
        results["Steve Shreve"]["Initial Capital"] = (
            results["Steve Shreve"]["K2"] + results["Steve Shreve"]["K3"] - 
            results["Steve Shreve"]["K1"] - results["Steve Shreve"]["K4"]
        )
        results["Drift-Adjusted"]["Initial Capital"] = (
            results["Drift-Adjusted"]["K2"] + results["Drift-Adjusted"]["K3"] - 
            results["Drift-Adjusted"]["K1"] - results["Drift-Adjusted"]["K4"]
        )
    elif strategy == "Straddle":
        results["CRR"]["Initial Capital"] = -(results["CRR"]["K1"] * 2)
        results["Steve Shreve"]["Initial Capital"] = -(results["Steve Shreve"]["K1"] * 2)
        results["Drift-Adjusted"]["Initial Capital"] = -(results["Drift-Adjusted"]["K1"] * 2)
    elif strategy == "Strangle":
        results["CRR"]["Initial Capital"] = -(results["CRR"]["K1"] + results["CRR"]["K2"])
        results["Steve Shreve"]["Initial Capital"] = -(results["Steve Shreve"]["K1"] + results["Steve Shreve"]["K2"])
        results["Drift-Adjusted"]["Initial Capital"] = -(results["Drift-Adjusted"]["K1"] + results["Drift-Adjusted"]["K2"])
    
    # Run GBM simulation
    gbm = GBM(mu=mu, sigma=sigma, n_steps=N, n_paths=n_paths, S0=S, T=T)
    paths = gbm.get_all_paths()
    final_prices = gbm.get_final_prices()
    
    # Calculate payouts from GBM simulation
    if strategy == "Iron Condor":
        payout_calc = IronCondorPayout(K1, K2, K3, K4)
    elif strategy == "Straddle":
        payout_calc = StraddlePayout(K1)
    elif strategy == "Strangle":
        payout_calc = StranglePayout(K1, K2)
    
    payout_values = payout_calc.calculate_payout(final_prices)
    avg_payout = np.mean(payout_values)
    
    # Calculate GBM expected value (Q-measure from simulation)
    results["CRR"]["GBM Expected Value"] = results["CRR"]["Initial Capital"] - avg_payout
    results["Steve Shreve"]["GBM Expected Value"] = results["Steve Shreve"]["Initial Capital"] - avg_payout
    results["Drift-Adjusted"]["GBM Expected Value"] = results["Drift-Adjusted"]["Initial Capital"] - avg_payout
    
    # Real-world probability analysis (P-measure)
    crr_rw = CoxRossRubinsteinRW(S, mu, r, sigma, T, N, K1, K2, K3, K4)
    shreve_rw = SteveShreveRW(S, mu, r, sigma, T, N, K1, K2, K3, K4)
    drift_rw = DriftAdjustedRW(S, mu, r, sigma, T, N, K1, K2, K3, K4)
    
    # Calculate RW expected profits
    results["CRR"]["RW Expected Value"] = crr_rw.get_exp_profits(
        results["CRR"]["Initial Capital"], 
        payout_name
    )
    results["Steve Shreve"]["RW Expected Value"] = shreve_rw.get_exp_profits(
        results["Steve Shreve"]["Initial Capital"], 
        payout_name
    )
    results["Drift-Adjusted"]["RW Expected Value"] = drift_rw.get_exp_profits(
        results["Drift-Adjusted"]["Initial Capital"], 
        payout_name
    )
    
    # Calculate probability of profit (only for Iron Condor)
    if strategy == "Iron Condor":
        results["CRR"]["Probability of Profit"] = crr_rw.get_prob_profit()
        results["Steve Shreve"]["Probability of Profit"] = shreve_rw.get_prob_profit()
        results["Drift-Adjusted"]["Probability of Profit"] = drift_rw.get_prob_profit()
    else:
        results["CRR"]["Probability of Profit"] = None
        results["Steve Shreve"]["Probability of Profit"] = None
        results["Drift-Adjusted"]["Probability of Profit"] = None
    
    # Store simulation data
    results["simulation"] = {
        "paths": paths,
        "final_prices": final_prices,
        "payout_values": payout_values
    }
    
    return results


def main():
    """Main application entry point."""
    setup_page_config()
    apply_custom_css()
    
    st.title("Options Simulator")
    st.markdown("""
        Compare risk-neutral pricing with real-world profitability analysis for options strategies.
    """)
    
    st.divider()
    
    # Initialize session state
    if "calculated" not in st.session_state:
        st.session_state.calculated = False
    if "results" not in st.session_state:
        st.session_state.results = None
    if "optimized" not in st.session_state:
        st.session_state.optimized = False
    if "opt_results" not in st.session_state:
        st.session_state.opt_results = None
    
    # Render sidebar and get inputs
    inputs = render_sidebar()
    st.session_state.inputs = inputs
    
    # Add optimization button
    optimize_button, grid_size = display_optimization_button(inputs)
    
    # Calculate button
    if st.sidebar.button("Calculate", type="primary"):
        with st.spinner("Calculating prices and running simulations..."):
            try:
                results = calculate_prices(inputs)
                st.session_state.results = results
                st.session_state.calculated = True
                st.rerun()
            except Exception as e:
                st.error(f"Calculation error: {str(e)}")
    
    # Optimization button logic
    if optimize_button:
        if not st.session_state.calculated or st.session_state.results is None:
            st.sidebar.error("Please calculate first before optimizing!")
        else:
            with st.spinner(f"Optimizing strikes ({grid_size} grid)... This may take a few minutes."):
                try:
                    # Get simulation data
                    final_prices = st.session_state.results["simulation"]["final_prices"]
                    
                    # Run optimization
                    opt_results = optimize_strikes(
                        S=inputs["S"],
                        r=inputs["r"],
                        T=inputs["T"],
                        sigma=inputs["sigma"],
                        mu=inputs["mu"],
                        final_prices=final_prices,
                        N=inputs["N"],
                        grid_size=grid_size,
                        payout_name='iron_condor'
                    )
                    
                    st.session_state.opt_results = opt_results
                    st.session_state.optimized = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Optimization error: {str(e)}")
    
    # Display results
    if st.session_state.calculated and st.session_state.results:
        st.success("Calculation complete!")
        
        st.subheader("Selected Parameters")
        param_col1, param_col2, param_col3 = st.columns(3)
        with param_col1:
            st.metric("Strategy", inputs["strategy"])
            st.metric("Stock Price", f"${inputs['S']:.2f}")
        with param_col2:
            st.metric("Volatility", f"{inputs['sigma']*100:.1f}%")
            st.metric("Risk-Free Rate", f"{inputs['r']*100:.1f}%")
        with param_col3:
            st.metric("Expected Return", f"{inputs['mu']*100:.1f}%")
            st.metric("Time to Expiry", f"{inputs['T']:.2f} years")
        
        st.divider()
        
        # Calculate average initial capital across models
        avg_initial_capital = (
            st.session_state.results["CRR"]["Initial Capital"] +
            st.session_state.results["Steve Shreve"]["Initial Capital"] +
            st.session_state.results["Drift-Adjusted"]["Initial Capital"]
        ) / 3
        
        # Create tabs for organized display
        tab1, tab2, tab3, tab4 = st.tabs([
            "Main Results",
            "Price Simulation", 
            "Payoff Diagram",
            "Distribution Analysis"
        ])
        
        with tab1:
            display_pricing_results(st.session_state.results)
            
            st.divider()
            
            display_summary_metrics(st.session_state.results, inputs)
            
            st.divider()
            
            display_q_vs_p_comparison(st.session_state.results, inputs)
            
            st.divider()
            
            display_profitability_insight(st.session_state.results, inputs)
        
        with tab2:
            plot_gbm_paths(st.session_state.results["simulation"], inputs)
            
            st.markdown("""
                **About this chart**: Shows simulated stock price paths using Geometric Brownian Motion.
                The strike prices are marked to show where the strategy becomes profitable or unprofitable.
            """)
        
        with tab3:
            plot_payout_diagram(inputs, avg_initial_capital)
            
            st.markdown("""
                **About this chart**: Shows the profit/loss profile of the strategy at different final prices.
                Breakeven points are marked with yellow diamonds.
            """)
        
        with tab4:
            plot_price_distribution(st.session_state.results["simulation"], inputs, avg_initial_capital)
            
            st.markdown("""
                **About this chart**: Histogram showing the distribution of simulated final prices.
                Green bars represent prices where the strategy is profitable, red bars show losses.
                The blue dashed line shows the theoretical lognormal distribution.
            """)
        
        # Add optimization results if available
        if st.session_state.optimized and st.session_state.opt_results:
            st.divider()
            
            display_optimization_summary_card(st.session_state.opt_results)
            
            with st.expander("Detailed Optimization Results", expanded=False):
                display_optimization_results(st.session_state.opt_results, inputs)
                
                st.divider()
                
                # Model selector for visualization
                st.markdown("### Visual Comparison")
                
                selected_model = st.selectbox(
                    "Select model to visualize",
                    options=['CRR', 'Steve Shreve', 'Drift-Adjusted'],
                    index=0
                )
                
                plot_optimal_comparison(inputs, st.session_state.opt_results, selected_model)
                
                st.divider()
                
                display_improvement_metrics(st.session_state.opt_results, st.session_state.results)
                
                st.divider()
                
                # Apply optimal strikes
                apply_clicked, optimal_strikes = display_apply_optimal_button(
                    st.session_state.opt_results,
                    selected_model
                )
                
                if apply_clicked and optimal_strikes:
                    st.session_state.inputs['K1'] = optimal_strikes[0]
                    st.session_state.inputs['K2'] = optimal_strikes[1]
                    st.session_state.inputs['K3'] = optimal_strikes[2]
                    st.session_state.inputs['K4'] = optimal_strikes[3]
                    st.success(f"Applied optimal strikes from {selected_model}! Scroll up and click Calculate to see results.")
        
    else:
        st.info("Configure your parameters in the sidebar and click Calculate to begin")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
                ### What this simulator does
                
                This tool helps you understand the critical difference between theoretical option pricing 
                and real-world profitability.
            """)
        
        with col2:
            st.markdown("""
                ### Quick Start
                
                1. Select strategy type
                2. Set strike prices
                3. Configure market parameters
                4. Click Calculate
                5. Analyze results
            """)


if __name__ == "__main__":
    main()
