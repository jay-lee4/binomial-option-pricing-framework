import streamlit as st
import pandas as pd


def display_pricing_results(results):
    """
    Display pricing results in a formatted DataFrame.
    
    Args:
        results: Dictionary containing pricing results from all models
    """
    st.subheader("Pricing & Profitability Results")
    
    models = ["CRR", "Steve Shreve", "Drift-Adjusted"]
    
    df_data = []
    for model in models:
        row = {
            "Model": model,
            "K1 Price": f"${results[model].get('K1', 0):.4f}",
            "K2 Price": f"${results[model].get('K2', 0):.4f}",
            "K3 Price": f"${results[model].get('K3', 0):.4f}",
            "K4 Price": f"${results[model].get('K4', 0):.4f}",
            "Initial Capital": f"${results[model]['Initial Capital']:.4f}",
            "GBM Expected": f"${results[model]['GBM Expected Value']:.4f}",
            "RW Expected": f"${results[model]['RW Expected Value']:.4f}"
        }
        
        if results[model]['Probability of Profit'] is not None:
            row["Prob. Profit"] = f"{results[model]['Probability of Profit']*100:.2f}%"
        else:
            row["Prob. Profit"] = "N/A"
        
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("""
        **Initial Capital**: Premium collected (or paid) when opening position  
        **GBM Expected**: Expected profit from Monte Carlo simulation (Q-measure)  
        **RW Expected**: Expected profit under real-world probabilities (P-measure)  
        **Prob. Profit**: Probability of profit under real-world measure
    """)


def display_summary_metrics(results, inputs):
    """
    Display summary metrics in metric cards.
    
    Args:
        results: Dictionary containing pricing results
        inputs: Dictionary of user inputs
    """
    st.subheader("Summary Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "CRR Initial Capital",
            f"${results['CRR']['Initial Capital']:.2f}",
            help="Premium for CRR model"
        )
        st.metric(
            "CRR Expected Profit (GBM)",
            f"${results['CRR']['GBM Expected Value']:.2f}",
            help="Expected profit from simulation"
        )
        st.metric(
            "CRR Expected Profit (RW)",
            f"${results['CRR']['RW Expected Value']:.2f}",
            delta=f"{results['CRR']['RW Expected Value'] - results['CRR']['GBM Expected Value']:.2f}",
            help="Expected profit under real-world probability"
        )
    
    with col2:
        st.metric(
            "Steve Shreve Initial Capital",
            f"${results['Steve Shreve']['Initial Capital']:.2f}",
            help="Premium for Steve Shreve model"
        )
        st.metric(
            "Steve Shreve Expected Profit (GBM)",
            f"${results['Steve Shreve']['GBM Expected Value']:.2f}",
            help="Expected profit from simulation"
        )
        st.metric(
            "Steve Shreve Expected Profit (RW)",
            f"${results['Steve Shreve']['RW Expected Value']:.2f}",
            delta=f"{results['Steve Shreve']['RW Expected Value'] - results['Steve Shreve']['GBM Expected Value']:.2f}",
            help="Expected profit under real-world probability"
        )
    
    with col3:
        st.metric(
            "Drift-Adjusted Initial Capital",
            f"${results['Drift-Adjusted']['Initial Capital']:.2f}",
            help="Premium for Drift-Adjusted model"
        )
        st.metric(
            "Drift-Adjusted Expected Profit (GBM)",
            f"${results['Drift-Adjusted']['GBM Expected Value']:.2f}",
            help="Expected profit from simulation"
        )
        st.metric(
            "Drift-Adjusted Expected Profit (RW)",
            f"${results['Drift-Adjusted']['RW Expected Value']:.2f}",
            delta=f"{results['Drift-Adjusted']['RW Expected Value'] - results['Drift-Adjusted']['GBM Expected Value']:.2f}",
            help="Expected profit under real-world probability"
        )


def display_q_vs_p_comparison(results, inputs):
    """
    Display comparison between Q-measure and P-measure results.
    
    Args:
        results: Dictionary containing pricing results
        inputs: Dictionary of user inputs
    """
    st.subheader("Q-Measure vs P-Measure Analysis")
    
    st.markdown("""
        **Key Insight**: Risk-neutral pricing (Q-measure) gives fair market prices, 
        but real-world profitability (P-measure) depends on actual market drift (μ).
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Q-Measure (Risk-Neutral)")
        st.markdown(f"""
        - Uses risk-free rate: **{inputs['r']*100:.1f}%**
        - Standard pricing framework
        - Ensures no-arbitrage
        - Based on GBM simulation
        """)
        
        st.markdown("**GBM Expected Values:**")
        for model in ["CRR", "Steve Shreve", "Drift-Adjusted"]:
            st.write(f"- {model}: ${results[model]['GBM Expected Value']:.2f}")
    
    with col2:
        st.markdown("### P-Measure (Real-World)")
        st.markdown(f"""
        - Uses expected return: **{inputs['mu']*100:.1f}%**
        - Actual market dynamics
        - Reveals true profitability
        - Based on binomial probabilities
        """)
        
        st.markdown("**RW Expected Values:**")
        for model in ["CRR", "Steve Shreve", "Drift-Adjusted"]:
            st.write(f"- {model}: ${results[model]['RW Expected Value']:.2f}")
    
    st.divider()
    
    if results["CRR"]["Probability of Profit"] is not None:
        st.markdown("### Probability of Profit (Iron Condor)")
        
        prob_col1, prob_col2, prob_col3 = st.columns(3)
        
        with prob_col1:
            prob_val = results["CRR"]["Probability of Profit"] * 100
            st.metric(
                "CRR",
                f"{prob_val:.2f}%",
                help="Probability of profit under real-world measure"
            )
        
        with prob_col2:
            prob_val = results["Steve Shreve"]["Probability of Profit"] * 100
            st.metric(
                "Steve Shreve",
                f"{prob_val:.2f}%",
                help="Probability of profit under real-world measure"
            )
        
        with prob_col3:
            prob_val = results["Drift-Adjusted"]["Probability of Profit"] * 100
            st.metric(
                "Drift-Adjusted",
                f"{prob_val:.2f}%",
                help="Probability of profit under real-world measure"
            )
        
        st.info("""
            **Interpretation**: This probability represents the likelihood that the stock price 
            stays within the profit zone at expiration, calculated using real-world drift (μ).
        """)


def display_profitability_insight(results, inputs):
    """
    Display key profitability insight based on results.
    
    Args:
        results: Dictionary containing pricing results
        inputs: Dictionary of user inputs
    """
    st.subheader("Profitability Analysis")
    
    avg_rw_profit = sum(results[m]["RW Expected Value"] for m in ["CRR", "Steve Shreve", "Drift-Adjusted"]) / 3
    
    if avg_rw_profit > 0:
        st.success(f"""
            **Strategy appears PROFITABLE under real-world dynamics**
            
            Average RW Expected Profit: ${avg_rw_profit:.2f}
            
            The expected return (μ = {inputs['mu']*100:.1f}%) suggests this strategy 
            should be profitable on average when held to expiration.
        """)
    elif avg_rw_profit < -0.5:
        st.error(f"""
            **Strategy appears UNPROFITABLE under real-world dynamics**
            
            Average RW Expected Profit: ${avg_rw_profit:.2f}
            
            The expected return (μ = {inputs['mu']*100:.1f}%) suggests this strategy 
            will likely result in a loss when held to expiration.
        """)
    else:
        st.warning(f"""
            **Strategy is approximately BREAK-EVEN under real-world dynamics**
            
            Average RW Expected Profit: ${avg_rw_profit:.2f}
            
            The strategy is roughly fairly priced given the market dynamics.
        """)
