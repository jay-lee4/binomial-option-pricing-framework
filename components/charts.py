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
    
    # Add strike price lines with legend
    fig.add_hline(
        y=K1, 
        line_dash="dash", 
        line_color="red",
        line_width=2,
        annotation_text=f"${K1:.0f}",
        annotation_position="top left"
    )
    
    fig.add_hline(
        y=K2, 
        line_dash="dash", 
        line_color="orange",
        line_width=2,
        annotation_text=f"${K2:.0f}",
        annotation_position="top left"
    )
    
    fig.add_hline(
        y=K3, 
        line_dash="dash", 
        line_color="orange",
        line_width=2,
        annotation_text=f"${K3:.0f}",
        annotation_position="top left"
    )
    
    fig.add_hline(
        y=K4, 
        line_dash="dash", 
        line_color="red",
        line_width=2,
        annotation_text=f"${K4:.0f}",
        annotation_position="top left"
    )
    
    # Add initial price line
    fig.add_hline(
        y=S,
        line_dash="solid",
        line_color="green",
        line_width=2,
        annotation_text=f"${S:.0f}",
        annotation_position="bottom left"
    )
    
    # Add invisible traces for legend
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='green', width=2, dash='solid'),
        name='Current Price (S0)'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='orange', width=2, dash='dash'),
        name='Short Strikes (K2, K3)'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Long Strikes (K1, K4)'
    ))
    
    fig.update_layout(
        title=f"Geometric Brownian Motion: {n_paths} Price Paths",
        xaxis_title="Time (Years)",
        yaxis_title="Stock Price ($)",
        hovermode='closest',
        template='plotly_white',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
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


def plot_payout_diagram(inputs, initial_capital):
    """
    Plot the profit/loss diagram for the strategy.
    
    Args:
        inputs: Dictionary of user inputs
        initial_capital: Premium collected/paid (average across models)
    """
    st.subheader("Strategy Payoff Diagram")
    
    strategy = inputs["strategy"]
    K1 = inputs["K1"]
    K2 = inputs["K2"]
    K3 = inputs["K3"]
    K4 = inputs["K4"]
    S = inputs["S"]
    
    price_range_min = min(K1, S) * 0.7
    price_range_max = max(K4, S) * 1.3
    final_prices = np.linspace(price_range_min, price_range_max, 200)
    
    from src.payouts import IronCondorPayout, StraddlePayout, StranglePayout
    
    if strategy == "Iron Condor":
        payout_calc = IronCondorPayout(K1, K2, K3, K4)
    elif strategy == "Straddle":
        payout_calc = StraddlePayout(K1)
    elif strategy == "Strangle":
        payout_calc = StranglePayout(K1, K2)
    
    payouts = payout_calc.calculate_payout(final_prices)
    profits = initial_capital - payouts
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=final_prices,
        y=profits,
        mode='lines',
        line=dict(width=3, color='blue'),
        fill='tozeroy',
        fillcolor='rgba(100, 150, 200, 0.2)',
        name='Profit/Loss',
        hovertemplate='Price: $%{x:.2f}<br>P/L: $%{y:.2f}<extra></extra>'
    ))
    
    fig.add_hline(
        y=0,
        line_dash="solid",
        line_color="black",
        line_width=2,
        annotation_text="Break-even",
        annotation_position="top right"
    )
    
    if strategy == "Iron Condor":
        fig.add_vline(x=K1, line_dash="dash", line_color="red", line_width=1.5,
                     annotation_text=f"K1: ${K1:.0f}", annotation_position="top")
        fig.add_vline(x=K2, line_dash="dash", line_color="orange", line_width=1.5,
                     annotation_text=f"K2: ${K2:.0f}", annotation_position="top")
        fig.add_vline(x=K3, line_dash="dash", line_color="orange", line_width=1.5,
                     annotation_text=f"K3: ${K3:.0f}", annotation_position="top")
        fig.add_vline(x=K4, line_dash="dash", line_color="red", line_width=1.5,
                     annotation_text=f"K4: ${K4:.0f}", annotation_position="top")
    elif strategy == "Straddle":
        fig.add_vline(x=K1, line_dash="dash", line_color="purple", line_width=1.5,
                     annotation_text=f"Strike: ${K1:.0f}", annotation_position="top")
    elif strategy == "Strangle":
        fig.add_vline(x=K1, line_dash="dash", line_color="red", line_width=1.5,
                     annotation_text=f"Put: ${K1:.0f}", annotation_position="top")
        fig.add_vline(x=K2, line_dash="dash", line_color="red", line_width=1.5,
                     annotation_text=f"Call: ${K2:.0f}", annotation_position="top")
    
    fig.add_vline(
        x=S,
        line_dash="solid",
        line_color="green",
        line_width=2,
        annotation_text=f"Current: ${S:.0f}",
        annotation_position="bottom"
    )
    
    breakeven_indices = np.where(np.diff(np.sign(profits)))[0]
    if len(breakeven_indices) > 0:
        for idx in breakeven_indices:
            be_price = final_prices[idx]
            fig.add_scatter(
                x=[be_price],
                y=[0],
                mode='markers',
                marker=dict(size=10, color='yellow', symbol='diamond'),
                name=f'Breakeven: ${be_price:.2f}',
                hovertemplate=f'Breakeven<br>Price: ${be_price:.2f}<extra></extra>'
            )
    
    fig.update_layout(
        title=f"{strategy} Payoff Diagram",
        xaxis_title="Final Stock Price ($)",
        yaxis_title="Profit/Loss ($)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    max_profit = np.max(profits)
    max_loss = np.min(profits)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Profit", f"${max_profit:.2f}")
    with col2:
        st.metric("Max Loss", f"${max_loss:.2f}")
    with col3:
        if len(breakeven_indices) > 0:
            st.metric("Breakeven Points", len(breakeven_indices))
        else:
            st.metric("Breakeven Points", "None")
