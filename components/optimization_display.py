import streamlit as st
import pandas as pd
import numpy as np


def display_optimization_button(inputs):
    """
    Display optimization button and settings.
    
    Args:
        inputs: Dictionary of user inputs
        
    Returns:
        Tuple of (should_optimize, grid_size)
    """
    st.sidebar.divider()
    st.sidebar.subheader("Optimization")
    
    st.sidebar.markdown("""
        Find optimal strike prices that maximize expected profit.
    """)
    
    grid_size = st.sidebar.selectbox(
        "Search Grid Size",
        options=['small', 'medium', 'large'],
        index=1,
        help="Larger grids take longer but may find better strikes"
    )
    
    grid_info = {
        'small': '~50-100 combinations (30 sec)',
        'medium': '~200-400 combinations (1-2 min)',
        'large': '~500-1000 combinations (3-5 min)'
    }
    
    st.sidebar.info(f"**{grid_size.title()}**: {grid_info[grid_size]}")
    
    optimize_button = st.sidebar.button(
        "Find Optimal Strikes",
        type="secondary",
        help="Search for strikes that maximize profit"
    )
    
    return optimize_button, grid_size


def display_optimization_results(opt_results, inputs):
    """
    Display optimization results in a comprehensive format.
    
    Args:
        opt_results: Dictionary containing optimization results
        inputs: Dictionary of user inputs
    """
    st.subheader("Optimization Results")
    
    st.markdown("""
        The optimizer searched through hundreds of strike price combinations to find the optimal strikes
        that maximize expected profit under both GBM simulation and real-world probabilities.
    """)
    
    # Create comparison table
    st.markdown("### Optimal Strikes Comparison")
    
    models = ['CRR', 'Steve Shreve', 'Drift-Adjusted']
    
    # GBM Optimal Strikes
    st.markdown("#### GBM-Optimized Strikes (Q-Measure)")
    
    gbm_data = []
    for model in models:
        k1, k2, k3, k4 = opt_results[model]['GBM_optimal_strikes']
        gbm_data.append({
            'Model': model,
            'K1': f'${k1:.0f}',
            'K2': f'${k2:.0f}',
            'K3': f'${k3:.0f}',
            'K4': f'${k4:.0f}',
            'Expected Profit': f"${opt_results[model]['GBM_max_profit']:.2f}"
        })
    
    gbm_df = pd.DataFrame(gbm_data)
    st.dataframe(gbm_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # RW Optimal Strikes
    st.markdown("#### Real-World Optimized Strikes (P-Measure)")
    
    rw_data = []
    for model in models:
        k1, k2, k3, k4 = opt_results[model]['RW_optimal_strikes']
        row = {
            'Model': model,
            'K1': f'${k1:.0f}',
            'K2': f'${k2:.0f}',
            'K3': f'${k3:.0f}',
            'K4': f'${k4:.0f}',
            'Expected Profit': f"${opt_results[model]['RW_max_profit']:.2f}"
        }
        
        if opt_results[model]['RW_prob_profit'] is not None:
            row['Prob. Profit'] = f"{opt_results[model]['RW_prob_profit']*100:.1f}%"
        
        rw_data.append(row)
    
    rw_df = pd.DataFrame(rw_data)
    st.dataframe(rw_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Key insights
    st.markdown("### Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### GBM Optimization")
        avg_gbm_profit = sum(opt_results[m]['GBM_max_profit'] for m in models) / 3
        st.metric("Avg Expected Profit", f"${avg_gbm_profit:.2f}")
        
        # Show which model performed best
        best_gbm_model = max(models, key=lambda m: opt_results[m]['GBM_max_profit'])
        best_gbm_profit = opt_results[best_gbm_model]['GBM_max_profit']
        st.info(f"**Best Model**: {best_gbm_model}\n\nExpected Profit: ${best_gbm_profit:.2f}")
    
    with col2:
        st.markdown("#### Real-World Optimization")
        avg_rw_profit = sum(opt_results[m]['RW_max_profit'] for m in models) / 3
        st.metric("Avg Expected Profit", f"${avg_rw_profit:.2f}")
        
        # Show which model performed best
        best_rw_model = max(models, key=lambda m: opt_results[m]['RW_max_profit'])
        best_rw_profit = opt_results[best_rw_model]['RW_max_profit']
        st.success(f"**Best Model**: {best_rw_model}\n\nExpected Profit: ${best_rw_profit:.2f}")
    
    st.divider()
    
    # Comparison with current strikes
    st.markdown("### Comparison with Current Strikes")
    
    current_strikes = (inputs['K1'], inputs['K2'], inputs['K3'], inputs['K4'])
    st.write(f"**Current Strikes**: K1=${current_strikes[0]:.0f}, K2=${current_strikes[1]:.0f}, "
             f"K3=${current_strikes[2]:.0f}, K4=${current_strikes[3]:.0f}")
    
    # Show improvement potential
    col1, col2, col3 = st.columns(3)
    
    for i, model in enumerate(models):
        with [col1, col2, col3][i]:
            rw_optimal = opt_results[model]['RW_optimal_strikes']
            improvement = opt_results[model]['RW_max_profit']
            
            if improvement > 0:
                st.success(f"**{model}**\n\nOptimal strikes could yield ${improvement:.2f} profit")
            else:
                st.warning(f"**{model}**\n\nOptimal strikes: ${improvement:.2f}")
    
    st.markdown("""
        ---
        **Note**: These are theoretical optimizations based on the selected parameters. 
        Actual results may vary due to market conditions, transaction costs, and other factors.
    """)


def display_optimization_summary_card(opt_results):
    """
    Display a compact summary card of optimization results.
    
    Args:
        opt_results: Dictionary containing optimization results
    """
    st.markdown("### Optimization Summary")
    
    # Get best RW model
    models = ['CRR', 'Steve Shreve', 'Drift-Adjusted']
    best_model = max(models, key=lambda m: opt_results[m]['RW_max_profit'])
    best_profit = opt_results[best_model]['RW_max_profit']
    best_strikes = opt_results[best_model]['RW_optimal_strikes']
    best_prob = opt_results[best_model]['RW_prob_profit']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Best Model", best_model)
    
    with col2:
        st.metric("Max Expected Profit", f"${best_profit:.2f}")
    
    with col3:
        if best_prob is not None:
            st.metric("Probability of Profit", f"{best_prob*100:.1f}%")
    
    st.info(f"""
        **Optimal Strikes for {best_model}**:  
        K1 = ${best_strikes[0]:.0f}, K2 = ${best_strikes[1]:.0f}, 
        K3 = ${best_strikes[2]:.0f}, K4 = ${best_strikes[3]:.0f}
    """)


def plot_optimal_comparison(current_inputs, opt_results, model_name='CRR'):
    """
    Plot side-by-side comparison of current vs optimal strikes.
    
    Args:
        current_inputs: Dictionary of current user inputs
        opt_results: Dictionary containing optimization results
        model_name: Which model to show (CRR, Steve Shreve, or Drift-Adjusted)
    """
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from src.payouts import IronCondorPayout
    
    # Current strikes
    current_k1 = current_inputs['K1']
    current_k2 = current_inputs['K2']
    current_k3 = current_inputs['K3']
    current_k4 = current_inputs['K4']
    
    # Optimal strikes
    opt_k1, opt_k2, opt_k3, opt_k4 = opt_results[model_name]['RW_optimal_strikes']
    
    S = current_inputs['S']
    
    # Generate price range
    price_range_min = min(current_k1, opt_k1, S) * 0.7
    price_range_max = max(current_k4, opt_k4, S) * 1.3
    final_prices = np.linspace(price_range_min, price_range_max, 200)
    
    # Calculate current payoff
    current_payout = IronCondorPayout(current_k1, current_k2, current_k3, current_k4)
    current_payout_values = current_payout.calculate_payout(final_prices)
    
    # Calculate optimal payoff
    optimal_payout = IronCondorPayout(opt_k1, opt_k2, opt_k3, opt_k4)
    optimal_payout_values = optimal_payout.calculate_payout(final_prices)
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Current Strikes', 'Optimal Strikes'),
        horizontal_spacing=0.15
    )
    
    # Current strikes plot
    fig.add_trace(
        go.Scatter(
            x=final_prices,
            y=-current_payout_values,
            mode='lines',
            line=dict(width=3, color='orange'),
            fill='tozeroy',
            fillcolor='rgba(255, 165, 0, 0.2)',
            name='Current',
            hovertemplate='Price: $%{x:.2f}<br>P/L: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Optimal strikes plot
    fig.add_trace(
        go.Scatter(
            x=final_prices,
            y=-optimal_payout_values,
            mode='lines',
            line=dict(width=3, color='green'),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 0, 0.2)',
            name='Optimal',
            hovertemplate='Price: $%{x:.2f}<br>P/L: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Add current price lines
    fig.add_vline(x=S, line_dash="solid", line_color="blue", line_width=2, row=1, col=1)
    fig.add_vline(x=S, line_dash="solid", line_color="blue", line_width=2, row=1, col=2)
    
    # Add strike lines for current
    fig.add_vline(x=current_k1, line_dash="dash", line_color="red", line_width=1, row=1, col=1)
    fig.add_vline(x=current_k2, line_dash="dash", line_color="orange", line_width=1, row=1, col=1)
    fig.add_vline(x=current_k3, line_dash="dash", line_color="orange", line_width=1, row=1, col=1)
    fig.add_vline(x=current_k4, line_dash="dash", line_color="red", line_width=1, row=1, col=1)
    
    # Add strike lines for optimal
    fig.add_vline(x=opt_k1, line_dash="dash", line_color="red", line_width=1, row=1, col=2)
    fig.add_vline(x=opt_k2, line_dash="dash", line_color="orange", line_width=1, row=1, col=2)
    fig.add_vline(x=opt_k3, line_dash="dash", line_color="orange", line_width=1, row=1, col=2)
    fig.add_vline(x=opt_k4, line_dash="dash", line_color="red", line_width=1, row=1, col=2)
    
    # Update layout
    fig.update_xaxes(title_text="Final Stock Price ($)", row=1, col=1)
    fig.update_xaxes(title_text="Final Stock Price ($)", row=1, col=2)
    fig.update_yaxes(title_text="Profit/Loss ($)", row=1, col=1)
    fig.update_yaxes(title_text="Profit/Loss ($)", row=1, col=2)
    
    fig.update_layout(
        height=500,
        showlegend=True,
        template='plotly_white',
        title_text=f"Payoff Comparison - {model_name}"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show strike comparison table
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current Strikes**")
        st.write(f"K1: ${current_k1:.0f}, K2: ${current_k2:.0f}, K3: ${current_k3:.0f}, K4: ${current_k4:.0f}")
    
    with col2:
        st.markdown("**Optimal Strikes**")
        st.write(f"K1: ${opt_k1:.0f}, K2: ${opt_k2:.0f}, K3: ${opt_k3:.0f}, K4: ${opt_k4:.0f}")


def display_improvement_metrics(opt_results, current_results):
    """
    Display improvement metrics comparing current vs optimal.
    
    Args:
        opt_results: Optimization results
        current_results: Current calculation results
    """
    st.markdown("### Improvement Analysis")
    
    models = ['CRR', 'Steve Shreve', 'Drift-Adjusted']
    
    for model in models:
        with st.expander(f"{model} Improvement", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            current_rw = current_results[model]['RW Expected Value']
            optimal_rw = opt_results[model]['RW_max_profit']
            improvement = optimal_rw - current_rw
            improvement_pct = (improvement / abs(current_rw)) * 100 if current_rw != 0 else 0
            
            with col1:
                st.metric("Current RW Profit", f"${current_rw:.2f}")
            
            with col2:
                st.metric("Optimal RW Profit", f"${optimal_rw:.2f}")
            
            with col3:
                st.metric(
                    "Improvement",
                    f"${improvement:.2f}",
                    delta=f"{improvement_pct:.1f}%"
                )
            
            if improvement > 0:
                st.success(f"Optimal strikes improve expected profit by ${improvement:.2f}")
            elif improvement < -0.5:
                st.error(f"Current strikes are better by ${abs(improvement):.2f}")
            else:
                st.info("Strikes are approximately optimal")


def display_apply_optimal_button(opt_results, model_name='CRR'):
    """
    Display button to apply optimal strikes to current configuration.
    
    Args:
        opt_results: Optimization results
        model_name: Which model's optimal strikes to apply
        
    Returns:
        True if button was clicked
    """
    st.markdown("### Apply Optimal Strikes")
    
    st.info(f"""
        Click below to update the sidebar parameters with the optimal strikes from **{model_name}**.
        This will replace your current strike prices.
    """)
    
    opt_k1, opt_k2, opt_k3, opt_k4 = opt_results[model_name]['RW_optimal_strikes']
    
    st.write(f"**Optimal strikes**: K1=${opt_k1:.0f}, K2=${opt_k2:.0f}, K3=${opt_k3:.0f}, K4=${opt_k4:.0f}")
    
    if st.button(f"Apply {model_name} Optimal Strikes", type="primary"):
        return True, (opt_k1, opt_k2, opt_k3, opt_k4)
    
    return False, None
