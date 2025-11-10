import streamlit as st


def display_help_section():
    """Display comprehensive help and documentation."""
    
    st.markdown("## Help & Documentation")
    
    # Create tabs for different help topics
    help_tab1, help_tab2, help_tab3, help_tab4 = st.tabs([
        "Getting Started",
        "Pricing Models",
        "Optimization",
        "Formulas"
    ])
    
    with help_tab1:
        display_getting_started()
    
    with help_tab2:
        display_pricing_models_info()
    
    with help_tab3:
        display_optimization_info()
    
    with help_tab4:
        display_formulas()


def display_getting_started():
    """Display getting started guide."""
    
    st.markdown("""
    ### Getting Started with the Options Simulator
    
    #### Basic Workflow
    
    1. **Select Strategy**: Choose between Iron Condor, Straddle, or Strangle
    2. **Set Strike Prices**: Configure K1, K2, K3, K4 based on your strategy
    3. **Configure Market Parameters**:
       - Stock Price (S): Current underlying price
       - Risk-Free Rate (r): Treasury rate
       - Expected Return (μ): Your view on stock returns
       - Volatility (σ): Annualized volatility
       - Time to Expiry (T): In years
    4. **Click Calculate**: Run the simulation and pricing
    5. **Analyze Results**: Review pricing, profitability, and charts
    6. **Optional - Optimize**: Find optimal strike prices
    
    #### Strategy Types
    
    **Iron Condor**
    - Sell K2 put and K3 call
    - Buy K1 put and K4 call
    - Profit if price stays between K2 and K3
    - Limited risk, limited reward
    
    **Straddle**
    - Buy both call and put at same strike (K1)
    - Profit from large price movements
    - Unlimited upside, high cost
    
    **Strangle**
    - Buy put at K1 and call at K2
    - Similar to straddle but cheaper
    - Requires larger price move to profit
    
    #### Key Metrics
    
    - **Initial Capital**: Premium received (positive) or paid (negative)
    - **GBM Expected Value**: Expected profit from Monte Carlo simulation
    - **RW Expected Value**: Expected profit under real-world probabilities
    - **Probability of Profit**: Chance of profit at expiration
    """)


def display_pricing_models_info():
    """Display information about pricing models."""
    
    st.markdown("""
    ### Pricing Models Explained
    
    The simulator uses three binomial tree models to price options:
    
    #### Cox-Ross-Rubinstein (CRR)
    
    - **Standard industry model**
    - Uses risk-neutral probabilities
    - Up/down factors based on volatility
    - Most commonly taught in textbooks
    
    **Key Features:**
    - Simple to implement
    - Converges to Black-Scholes
    - Risk-neutral framework (Q-measure)
    
    #### Steve Shreve Model
    
    - **Alternative binomial approach**
    - Different up/down factor calculation
    - Also risk-neutral
    - Named after Steven Shreve (CMU professor)
    
    **Key Features:**
    - Slightly different tree structure
    - Faster convergence in some cases
    - Popular in academic settings
    
    #### Drift-Adjusted Model
    
    - **Incorporates expected return (μ)**
    - Uses real-world drift instead of risk-free rate
    - Still uses binomial tree framework
    - Better for P-measure analysis
    
    **Key Features:**
    - Reflects actual expected returns
    - Not arbitrage-free
    - Useful for personal trading decisions
    
    #### Q-Measure vs P-Measure
    
    **Q-Measure (Risk-Neutral)**
    - Used by CRR and Shreve
    - Prices for fair market value
    - Uses risk-free rate (r)
    - Ensures no arbitrage
    
    **P-Measure (Real-World)**
    - Used in profitability analysis
    - Based on actual expected returns (μ)
    - Shows true profit expectations
    - Accounts for market drift
    
    The key insight: Risk-neutral prices are fair, but real-world profitability 
    depends on whether μ > r or μ < r.
    """)


def display_optimization_info():
    """Display optimization information."""
    
    st.markdown("""
    ### Strike Price Optimization
    
    The optimizer searches through hundreds of strike price combinations to find 
    the configuration that maximizes expected profit.
    
    #### How It Works
    
    1. **Generate Grid**: Creates combinations of K1, K2, K3, K4
    2. **Calculate Prices**: Prices each combination with all three models
    3. **Simulate Outcomes**: Tests each against GBM simulation
    4. **Rank Results**: Finds strikes with highest expected profit
    5. **Report Best**: Shows optimal strikes for both Q and P measures
    
    #### Grid Sizes
    
    - **Small**: ~50-100 combinations, 30 seconds
    - **Medium**: ~200-400 combinations, 1-2 minutes
    - **Large**: ~500-1000 combinations, 3-5 minutes
    
    Larger grids explore more possibilities but take longer.
    
    #### Optimization Criteria
    
    The optimizer maximizes:
    - **GBM Expected Profit**: Based on Monte Carlo simulation
    - **RW Expected Profit**: Based on real-world probability tree
    
    Both are calculated and reported separately, as they may suggest different 
    optimal strikes depending on the relationship between μ and r.
    
    #### Applying Results
    
    After optimization:
    1. Review the suggested strikes
    2. Compare current vs optimal payoff diagrams
    3. Check improvement metrics
    4. Click "Apply Optimal Strikes" to use them
    5. Recalculate to see full results
    
    #### Important Notes
    
    - Optimization assumes no transaction costs
    - Results are theoretical based on your parameters
    - Market conditions may differ from model assumptions
    - Always validate with your own analysis
    """)


def display_formulas():
    """Display mathematical formulas used."""
    
    st.markdown("""
    ### Mathematical Formulas
    
    #### Cox-Ross-Rubinstein Model
    
    **Up/Down Factors:**
```
    u = e^(σ√Δt)
    d = 1/u = e^(-σ√Δt)
```
    
    **Risk-Neutral Probability:**
```
    q = (e^(rΔt) - d) / (u - d)
```
    
    **Option Price:**
```
    V₀ = e^(-rT) * Σ [C(n,j) * q^j * (1-q)^(n-j) * max(payoff, 0)]
```
    
    #### Steve Shreve Model
    
    **Up/Down Factors:**
```
    u = e^((r - σ²/2)Δt + σ√Δt)
    d = e^((r - σ²/2)Δt - σ√Δt)
```
    
    **Risk-Neutral Probability:**
```
    q = (e^(rΔt) - d) / (u - d)
```
    
    #### Drift-Adjusted Model
    
    **Up/Down Factors:**
```
    u = e^(σ√Δt)
    d = 1/u
```
    
    **Real-World Probability:**
```
    p = (e^(μΔt) - d) / (u - d)
```
    
    #### Geometric Brownian Motion
    
    **Stock Price Evolution:**
```
    dS = μS dt + σS dW
    S(t) = S₀ * e^((μ - σ²/2)t + σW(t))
```
    
    Where W(t) is a Wiener process (Brownian motion).
    
    #### Iron Condor Payoff
```
    Payoff = max(K₁ - Sᴛ, 0) - max(K₂ - Sᴛ, 0)
           - max(Sᴛ - K₃, 0) + max(Sᴛ - K₄, 0)
```
    
    **Simplified:**
    - If Sᴛ < K₁: Loss = K₁ - Sᴛ
    - If K₁ ≤ Sᴛ < K₂: Loss = K₂ - Sᴛ
    - If K₂ ≤ Sᴛ ≤ K₃: No loss (profit = premium)
    - If K₃ < Sᴛ ≤ K₄: Loss = Sᴛ - K₃
    - If Sᴛ > K₄: Loss = K₄ - K₃
    
    #### Key Variables
    
    - S₀, S: Current/future stock price
    - K₁, K₂, K₃, K₄: Strike prices
    - r: Risk-free interest rate
    - μ: Expected return (drift)
    - σ: Volatility (standard deviation)
    - T: Time to expiration
    - Δt: Time step (T/N)
    - N: Number of binomial steps
    - q: Risk-neutral probability
    - p: Real-world probability
    """)


def display_quick_reference():
    """Display quick reference card."""
    
    st.sidebar.markdown("### Quick Reference")
    
    with st.sidebar.expander("Common Parameters"):
        st.markdown("""
        **Low Volatility**: 15-20%
        **Medium Volatility**: 20-35%
        **High Volatility**: 35%+
        
        **Risk-Free Rate**: 4-5% (2024)
        
        **Expected Return**:
        - Conservative: 6-8%
        - Moderate: 8-10%
        - Aggressive: 10-12%
        """)
    
    with st.sidebar.expander("Strategy Rules"):
        st.markdown("""
        **Iron Condor**: K₁ < K₂ < S < K₃ < K₄
        
        **Typical Widths**:
        - K₂ - K₁: 5-10% of S
        - K₄ - K₃: 5-10% of S
        - K₃ - K₂: 10-20% of S
        """)
