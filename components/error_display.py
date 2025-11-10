import streamlit as st


def display_validation_error(error_message: str):
    """
    Display validation error in a user-friendly way.
    
    Args:
        error_message: The error message to display
    """
    st.error(f"**Validation Error**\n\n{error_message}")
    
    st.markdown("""
        **Common Issues:**
        - Iron Condor: Ensure K1 < K2 < S < K3 < K4
        - Strike prices should be at least 2% away from current price
        - Volatility should be between 1% and 200%
        - Time to expiration should be between 4 days and 5 years
        
        **Need help?** Check the "Help & Export" tab for guidance.
    """)


def display_calculation_error(error: Exception):
    """
    Display calculation error with helpful context.
    
    Args:
        error: The exception that was raised
    """
    st.error(f"**Calculation Error**\n\n{str(error)}")
    
    with st.expander("Technical Details"):
        st.code(str(error))
        st.markdown("""
            **Possible Causes:**
            - Strike prices may be causing numerical instability
            - Simulation parameters may be too extreme
            - Market parameters may lead to invalid calculations
            
            **Suggested Actions:**
            1. Try using default parameters first
            2. Adjust strike prices to be more conservative
            3. Reduce the number of binomial steps if very high
            4. Check that all parameters are reasonable
        """)


def display_optimization_error(error: Exception):
    """
    Display optimization error with context.
    
    Args:
        error: The exception that was raised
    """
    st.error(f"**Optimization Error**\n\n{str(error)}")
    
    with st.expander("What went wrong?"):
        st.code(str(error))
        st.markdown("""
            **Optimization Failed:**
            - The grid search may have encountered invalid strike combinations
            - Some parameter combinations may cause numerical issues
            - Try a smaller grid size first
            
            **Suggested Actions:**
            1. Use "small" grid size to test
            2. Ensure current calculation works before optimizing
            3. Check that your parameters are reasonable
        """)


def display_warning_banner(message: str):
    """
    Display a warning banner.
    
    Args:
        message: Warning message
    """
    st.warning(f"⚠️ {message}")


def display_info_banner(message: str):
    """
    Display an info banner.
    
    Args:
        message: Info message
    """
    st.info(f"ℹ️ {message}")
