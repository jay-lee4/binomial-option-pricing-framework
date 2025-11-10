# Options Simulator

A comprehensive options pricing and profitability analysis tool that compares risk-neutral pricing with real-world profitability for options strategies.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

This simulator helps you understand the critical difference between theoretical option pricing (Q-measure) and real-world profitability (P-measure). It implements three binomial tree models and uses Monte Carlo simulation to analyze options strategies.

### Key Features

- **Three Pricing Models**: Cox-Ross-Rubinstein, Steve Shreve, and Drift-Adjusted
- **Multiple Strategies**: Iron Condor, Straddle, Strangle
- **Real-World Analysis**: Compare risk-neutral pricing vs actual profitability
- **Monte Carlo Simulation**: GBM-based price path simulation
- **Strike Optimization**: Find optimal strikes that maximize expected profit
- **Interactive Visualizations**: Charts for price paths, payoff diagrams, distributions
- **Data Export**: CSV and JSON export for all results
- **Comprehensive Help**: Built-in documentation and formulas

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/binomial-options-framework.git
cd binomial-options-framework
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Quick Start

1. **Select Strategy**: Choose Iron Condor, Straddle, or Strangle
2. **Set Strike Prices**: Configure K1, K2, K3, K4 (for Iron Condor)
3. **Configure Parameters**:
   - Stock Price (S): Current price
   - Risk-Free Rate (r): ~4-5%
   - Expected Return (μ): Your market view (6-12%)
   - Volatility (σ): Annualized volatility (15-35%)
   - Time to Expiry (T): In years
4. **Click Calculate**: Run pricing and simulation
5. **Analyze Results**: Review tabs for pricing, charts, and analysis
6. **Optimize** (optional): Find optimal strike prices

## Project Structure
```
binomial-options-framework/
├── app.py                      # Main Streamlit application
├── config/
│   └── settings.py            # Default parameters and configuration
├── src/
│   ├── models.py              # Binomial tree pricing models
│   ├── gbm.py                 # Geometric Brownian Motion simulation
│   ├── payouts.py             # Strategy payoff calculations
│   ├── analytics.py           # Real-world probability analysis
│   ├── optimize.py            # Strike price optimization
│   ├── export.py              # Data export utilities
│   └── validation.py          # Input validation
├── components/
│   ├── sidebar.py             # Sidebar input controls
│   ├── results_display.py     # Results tables and metrics
│   ├── charts.py              # Plotly visualizations
│   ├── optimization_display.py # Optimization results
│   ├── help_section.py        # Documentation and help
│   ├── export_display.py      # Export functionality
│   └── error_display.py       # Error handling displays
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Mathematical Background

### Pricing Models

#### Cox-Ross-Rubinstein (CRR)

The standard binomial model with:
- Up factor: `u = e^(σ√Δt)`
- Down factor: `d = 1/u`
- Risk-neutral probability: `q = (e^(rΔt) - d) / (u - d)`

#### Steve Shreve Model

Alternative binomial approach:
- Up factor: `u = e^((r - σ²/2)Δt + σ√Δt)`
- Down factor: `d = e^((r - σ²/2)Δt - σ√Δt)`
- Risk-neutral probability: `q = (e^(rΔt) - d) / (u - d)`

#### Drift-Adjusted Model

Incorporates real-world drift:
- Up factor: `u = e^(σ√Δt)`
- Down factor: `d = 1/u`
- Real-world probability: `p = (e^(μΔt) - d) / (u - d)`

### Q-Measure vs P-Measure

**Q-Measure (Risk-Neutral)**
- Uses risk-free rate (r)
- Prices for arbitrage-free market value
- Standard in derivatives pricing

**P-Measure (Real-World)**
- Uses expected return (μ)
- Reflects actual profit expectations
- Based on trader's market view

The key insight: Options may be fairly priced but still profitable (or unprofitable) depending on whether μ > r or μ < r.

## Usage Examples

### Basic Calculation
```python
# Default Iron Condor at-the-money
S = 100   # Stock price
K1 = 90   # Long put
K2 = 95   # Short put
K3 = 105  # Short call
K4 = 110  # Long call
r = 0.05  # Risk-free rate
μ = 0.08  # Expected return
σ = 0.20  # 20% volatility
T = 1.0   # 1 year to expiration
```

### Strategy Examples

#### Iron Condor
- Profit if price stays between K2 and K3
- Limited risk: Max loss = (K4 - K3) or (K2 - K1) minus premium
- Limited reward: Premium collected

#### Straddle
- Profit from large price movements in either direction
- Unlimited upside potential
- Cost: 2× at-the-money option premium

#### Strangle
- Similar to straddle but cheaper
- Requires larger move to profit
- Lower cost than straddle

## Testing

Run the test suite:
```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_models.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## Performance Tips

1. **Use Caching**: The app uses Streamlit caching to speed up repeated calculations
2. **Adjust Grid Size**: For optimization, start with "small" grid to test
3. **Reduce Paths**: Lower Monte Carlo paths for faster calculations (minimum 1000 recommended)
4. **Binomial Steps**: 100-500 steps usually sufficient for accurate pricing


## Known Limitations

- Assumes European-style options (exercise at expiration only)
- Does not include transaction costs or bid-ask spreads
- Optimization is computationally intensive for large grids
- Real-world results may vary due to market microstructure
- Early exercise features not implemented (American options)


## Future Enhancements

- [ ] American options with early exercise
- [ ] Greeks calculation (Delta, Gamma, Theta, Vega)
- [ ] Portfolio analysis (multiple positions)
- [ ] Historical volatility calculation from data
- [ ] Implied volatility solver
- [ ] Advanced strategies (Butterfly, Ratio spreads)
- [ ] Real-time data integration
- [ ] Backtesting framework


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments

- Binomial model theory from Cox, Ross, and Rubinstein (1979)
- Steve Shreve's "Stochastic Calculus for Finance" volumes
- NumPy and SciPy for numerical computation
- Streamlit for the web framework
- Plotly for interactive visualizations


## References

### Academic Papers
- Cox, J. C., Ross, S. A., & Rubinstein, M. (1979). "Option pricing: A simplified approach"
- Shreve, S. E. (2004). "Stochastic Calculus for Finance I & II"

### Books
- Hull, J. C. (2017). "Options, Futures, and Other Derivatives"
- Shreve, S. E. (2004). "Stochastic Calculus for Finance"

### Online Resources
- [Investopedia Options Guide](https://www.investopedia.com/options-basics-tutorial-4583012)
- [CBOE Options Education](https://www.cboe.com/education/)
