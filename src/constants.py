# Strike price validation
MIN_STRIKE_SEPARATION_PCT = 0.02  # Minimum 2% separation from current price
MIN_SPREAD_WIDTH = 1.0  # Minimum $1 width between adjacent strikes

# Volatility bounds
MIN_VOLATILITY = 0.01  # 1% minimum volatility
MAX_VOLATILITY = 2.0   # 200% maximum volatility (catch extreme inputs)

# Time to expiration bounds
MIN_TIME_TO_EXPIRY = 0.01  # ~4 days minimum
MAX_TIME_TO_EXPIRY = 5.0   # 5 years maximum

# Rate bounds
MIN_RISK_FREE_RATE = 0.0   # Allow zero but not negative
MAX_RISK_FREE_RATE = 0.20  # 20% maximum (catch typos)
MIN_EXPECTED_RETURN = -0.50  # -50% minimum
MAX_EXPECTED_RETURN = 0.50   # 50% maximum

# Stock price bounds
MIN_STOCK_PRICE = 1.0       # $1 minimum
MAX_STOCK_PRICE = 100000.0  # $100k maximum (catch typos)

# Simulation parameter bounds
MIN_BINOMIAL_STEPS = 10      # Too few steps = inaccurate
MAX_BINOMIAL_STEPS = 10000   # Too many steps = slow
MIN_MC_PATHS = 100           # Minimum for statistical significance
MAX_MC_PATHS = 100000        # Balance accuracy vs speed

# ============================================================================
# WARNING THRESHOLDS
# ============================================================================

# When to display warnings to users
HIGH_VOLATILITY_THRESHOLD = 0.50  # Warn if σ > 50%
LARGE_MU_R_DIFF_THRESHOLD = 0.10  # Warn if |μ - r| > 10%
SHORT_EXPIRY_THRESHOLD = 0.08     # Warn if T < 1 month

# ============================================================================
# OPTIMIZATION PARAMETERS
# ============================================================================

# Differential evolution settings
OPTIMIZATION_TOL = 1e-4            # Convergence tolerance
MAX_OPTIMIZATION_ITER = 1000       # Maximum iterations
OPTIMIZATION_SEED = 42             # Reproducibility

# Strike search bounds (as fraction of current price)
K1_LOWER_BOUND_PCT = 0.60  # K1 minimum: 60% of S
K1_UPPER_BOUND_PCT = 0.95  # K1 maximum: 95% of S
K2_LOWER_BOUND_PCT = 0.70  # K2 minimum: 70% of S
K2_UPPER_BOUND_PCT = 0.98  # K2 maximum: 98% of S
K3_LOWER_BOUND_PCT = 1.02  # K3 minimum: 102% of S
K3_UPPER_BOUND_PCT = 1.30  # K3 maximum: 130% of S
K4_LOWER_BOUND_PCT = 1.05  # K4 minimum: 105% of S
K4_UPPER_BOUND_PCT = 1.40  # K4 maximum: 140% of S

# Constraint enforcement
MIN_STRIKE_SEPARATION = 0.5  # Minimum $0.50 between adjacent strikes

# ============================================================================
# NUMERICAL PRECISION
# ============================================================================

PRICE_PRECISION = 1e-10  # Tolerance for price comparisons
PROBABILITY_PRECISION = 1e-10  # Tolerance for probability sums

# ============================================================================
# CACHING CONFIGURATION
# ============================================================================

# LRU cache sizes for expensive computations
TREE_PARAMS_CACHE_SIZE = 128  # Cache binomial tree parameters

# ============================================================================
# STRATEGY MAPPINGS
# ============================================================================

STRATEGY_TO_PAYOUT_NAME = {
    "Iron Condor": "iron_condor",
    "Straddle": "straddle",
    "Strangle": "strangle"
}

VALID_OPTION_TYPES = {'C', 'P'}  # Valid option types
