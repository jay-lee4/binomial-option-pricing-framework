import streamlit as st
from config.settings import DEFAULT_PARAMS
from components.sidebar import render_sidebar


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Options Simulator",
        page_icon="chart_with_upwards_trend",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown("""
        <style>
        .main {
            padding: 1rem 2rem;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 600;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            color: #6c757d;
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
        
        [data-testid="stSidebar"] {
            background-color: #f8fafc;
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #1e293b;
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
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1rem;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #eff6ff;
            border-bottom: 2px solid #3b82f6;
        }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    setup_page_config()
    apply_custom_css()
    
    st.title("Options Simulator")
    st.markdown("""
        Compare risk-neutral pricing with real-world profitability analysis for options strategies.
    """)
    
    st.divider()
    
    if "calculated" not in st.session_state:
        st.session_state.calculated = False
    if "results" not in st.session_state:
        st.session_state.results = None
    
    # Render sidebar and get inputs
    inputs = render_sidebar()
    
    # Store inputs in session state
    st.session_state.inputs = inputs
    
    # Calculate button
    if st.sidebar.button("Calculate", type="primary"):
        st.session_state.calculated = True
        st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.calculated:
            st.success("Calculation complete! Results will appear here.")
            
            # Display selected parameters
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
        else:
            st.info("Configure your parameters in the sidebar and click Calculate to begin")
            
            st.markdown("""
                ### What this simulator does
                
                This tool helps you understand the critical difference between theoretical option pricing 
                and real-world profitability:
                
                **Risk-Neutral Pricing (Q-measure)**
                - Uses risk-free rate for fair market valuation
                - Ensures no-arbitrage pricing
                - Standard Black-Scholes framework
                
                **Real-World Analysis (P-measure)**
                - Uses actual expected returns (drift)
                - Calculates true profit expectations
                - Reveals if strategies are actually profitable
                
                ### Models Included
                
                - **Cox-Ross-Rubinstein**: Standard exponential binomial tree
                - **Steve Shreve**: Linear approximation with symmetric probabilities  
                - **Drift-Adjusted**: Incorporates real-world drift in tree construction
            """)
    
    with col2:
        if st.session_state.calculated:
            st.info("Analysis complete")
        else:
            st.markdown("""
                ### Quick Start
                
                1. Select strategy type
                2. Set strike prices
                3. Configure market parameters
                4. Click Calculate
                5. Analyze Q vs P measure results
            """)


if __name__ == "__main__":
    main()
