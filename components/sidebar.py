import streamlit as st
from config.settings import DEFAULT_PARAMS, STRATEGY_INFO


def render_sidebar():
    """
    Render sidebar with all input parameters.
    
    Returns:
        dict: Dictionary containing all user inputs
    """
    st.sidebar.header("Configuration")
    
    # Strategy selection
    st.sidebar.subheader("Strategy")
    strategy = st.sidebar.selectbox(
        "Select Strategy",
        options=list(STRATEGY_INFO.keys()),
        help="Choose the options strategy to analyze"
    )
    
    # Show strategy description
    with st.sidebar.expander("Strategy Details"):
        st.markdown(f"**{strategy}**")
        st.write(STRATEGY_INFO[strategy]["description"])
        st.write(f"**Max Profit:** {STRATEGY_INFO[strategy]['max_profit']}")
        st.write(f"**Max Loss:** {STRATEGY_INFO[strategy]['max_loss']}")
    
    st.sidebar.divider()
    
    # Strike prices section
    st.sidebar.subheader("Strike Prices")
    
    if strategy == "Iron Condor":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            K1 = st.number_input(
                "K1 (Long Put)",
                min_value=1.0,
                value=DEFAULT_PARAMS["K1"],
                step=1.0,
                help="Lowest strike - buy put"
            )
            K2 = st.number_input(
                "K2 (Short Put)",
                min_value=1.0,
                value=DEFAULT_PARAMS["K2"],
                step=1.0,
                help="Lower middle strike - sell put"
            )
        with col2:
            K3 = st.number_input(
                "K3 (Short Call)",
                min_value=1.0,
                value=DEFAULT_PARAMS["K3"],
                step=1.0,
                help="Upper middle strike - sell call"
            )
            K4 = st.number_input(
                "K4 (Long Call)",
                min_value=1.0,
                value=DEFAULT_PARAMS["K4"],
                step=1.0,
                help="Highest strike - buy call"
            )
        
        # Validate strike ordering
        if not (K1 < K2 < K3 < K4):
            st.sidebar.error("Strikes must satisfy: K1 < K2 < K3 < K4")
    
    elif strategy == "Straddle":
        K1 = st.sidebar.number_input(
            "K (Strike Price)",
            min_value=1.0,
            value=DEFAULT_PARAMS["K1"],
            step=1.0,
            help="Strike price for both call and put"
        )
        K2, K3, K4 = K1, K1, K1
    
    elif strategy == "Strangle":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            K1 = st.number_input(
                "K_put",
                min_value=1.0,
                value=DEFAULT_PARAMS["K1"],
                step=1.0,
                help="Put strike price"
            )
        with col2:
            K2 = st.number_input(
                "K_call",
                min_value=1.0,
                value=DEFAULT_PARAMS["K3"],
                step=1.0,
                help="Call strike price"
            )
        
        if K1 >= K2:
            st.sidebar.error("Put strike must be less than call strike")
        
        K3, K4 = K2, K2
    
    st.sidebar.divider()
    
    # Market parameters section
    st.sidebar.subheader("Market Parameters")
    
    S = st.sidebar.number_input(
        "Current Stock Price (S)",
        min_value=1.0,
        value=DEFAULT_PARAMS["S"],
        step=1.0,
        help="Current price of the underlying asset"
    )
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        r = st.number_input(
            "Risk-Free Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=DEFAULT_PARAMS["r"] * 100,
            step=0.1,
            help="Annual risk-free interest rate"
        ) / 100
        
        sigma = st.number_input(
            "Volatility (%)",
            min_value=0.0,
            max_value=200.0,
            value=DEFAULT_PARAMS["sigma"] * 100,
            step=1.0,
            help="Annual volatility (standard deviation)"
        ) / 100
    
    with col2:
        mu = st.number_input(
            "Expected Return (%)",
            min_value=-100.0,
            max_value=200.0,
            value=DEFAULT_PARAMS["mu"] * 100,
            step=0.1,
            help="Real-world expected annual return (drift)"
        ) / 100
        
        T = st.number_input(
            "Time to Expiry (Years)",
            min_value=0.01,
            max_value=10.0,
            value=DEFAULT_PARAMS["T"],
            step=0.25,
            help="Time until option expiration"
        )
    
    st.sidebar.divider()
    
    # Simulation parameters
    with st.sidebar.expander("Advanced Settings"):
        N = st.number_input(
            "Binomial Steps",
            min_value=10,
            max_value=2000,
            value=DEFAULT_PARAMS["N"],
            step=50,
            help="Number of time steps in binomial tree"
        )
        
        n_paths = st.number_input(
            "GBM Paths",
            min_value=100,
            max_value=10000,
            value=DEFAULT_PARAMS["n_paths"],
            step=100,
            help="Number of price paths to simulate"
        )
    
    return {
        "strategy": strategy,
        "S": S,
        "K1": K1,
        "K2": K2,
        "K3": K3,
        "K4": K4,
        "T": T,
        "r": r,
        "sigma": sigma,
        "mu": mu,
        "N": N,
        "n_paths": n_paths
    }
