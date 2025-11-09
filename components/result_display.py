import streamlit as st
import pandas as pd


def display_pricing_results(results):
    """
    Display pricing results in a formatted DataFrame.
    
    Args:
        results: Dictionary containing pricing results from all models
    """
    st.subheader("Risk-Neutral Pricing Results")
    
    # Create DataFrame from results
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
            "GBM Expected Value": f"${results[model]['GBM Expected Value']:.4f}"
        }
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("""
        **Initial Capital**: Premium collected (or paid) when opening the position  
        **GBM Expected Value**: Expected profit based on simulated price paths
    """)


def display_summary_metrics(results, inputs):
    """    
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
            "CRR Expected Profit",
            f"${results['CRR']['GBM Expected Value']:.2f}",
            help="Expected profit from GBM simulation"
        )
    
    with col2:
        st.metric(
            "Steve Shreve Initial Capital",
            f"${results['Steve Shreve']['Initial Capital']:.2f}",
            help="Premium for Steve Shreve model"
        )
        st.metric(
            "Steve Shreve Expected Profit",
            f"${results['Steve Shreve']['GBM Expected Value']:.2f}",
            help="Expected profit from GBM simulation"
        )
    
    with col3:
        st.metric(
            "Drift-Adjusted Initial Capital",
            f"${results['Drift-Adjusted']['Initial Capital']:.2f}",
            help="Premium for Drift-Adjusted model"
        )
        st.metric(
            "Drift-Adjusted Expected Profit",
            f"${results['Drift-Adjusted']['GBM Expected Value']:.2f}",
            help="Expected profit from GBM simulation"
        )
