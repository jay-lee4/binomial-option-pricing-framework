import streamlit as st
import pandas as pd


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
