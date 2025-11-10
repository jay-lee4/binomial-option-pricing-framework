import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def plot_gbm_paths(simulation_data, inputs):
    """
    Plot GBM simulated price paths with strike prices.
    
    Args:
        simulation_data: Dictionary containing paths and prices
        inputs: Dictionary of user inputs
    """
    st.subheader("Simulated Price Paths")
    
    paths = simulation_data["paths"]
    S = inputs["S"]
    T = inputs["T"]
    K1 = inputs["K1"]
    K2 = inputs["K2"]
    K3 = inputs["K3"]
    K4 = inputs["K4"]
    
    n_paths, n_steps = paths.shape
    time_steps = np.linspace(0, T, n_steps)
    
    fig = go.Figure()
    
    # Plot a subset of paths to avoid clutter
    max_paths_to_show = min(50, n_paths)
    
    for i in range(max_paths_to_show):
        fig.add_trace(go.Scatter(
            x=time_steps,
            y=paths[i, :],
            mode='lines',
            line=dict(width=0.5, color='rgba(100, 150, 200, 0.3)'),
            showlegend=False,
            hovertemplate='Time: %{x:.2f}<br>Price: $%{y:.2f}<extra></extra>'
        ))
    
    # Add strike price lines
    fig.add_hline(
        y=K1, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"K1: ${K1:.2f}",
        annotation_position="right"
    )
    fig.add_hline(
        y=K2, 
        line_dash="dash", 
        line_color="orange",
        annotation_text=f"K2: ${K2:.2f}",
        annotation_position="right"
    )
    fig.add_hline(
        y=K3, 
        line_dash="dash", 
        line_color="orange",
        annotation_text=f"K3: ${K3:.2f}",
        annotation_position="right"
    )
    fig.add_hline(
        y=K4, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"K4: ${K4:.2f}",
        annotation_position="right"
    )
    
    # Add initial price line
    fig.add_hline(
        y=S,
        line_dash="solid",
        line_color="green",
        annotation_text=f"S0: ${S:.2f}",
        annotation_position="left"
    )
    
    fig.update_layout(
        title=f"Geometric Brownian Motion: {n_paths} Price Paths",
        xaxis_title="Time (Years)",
        yaxis_title="Stock Price ($)",
        hovermode='closest',
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add statistics
    final_prices = simulation_data["final_prices"]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mean Final Price", f"${np.mean(final_prices):.2f}")
    with col2:
        st.metric("Std Dev", f"${np.std(final_prices):.2f}")
    with col3:
        st.metric("Min Price", f"${np.min(final_prices):.2f}")
    with col4:
        st.metric("Max Price", f"${np.max(final_prices):.2f}")
