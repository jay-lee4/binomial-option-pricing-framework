DEFAULT_PARAMS = {
    "S": 100.0,
    "K1": 90.0,
    "K2": 95.0,
    "K3": 105.0,
    "K4": 110.0,
    "T": 1.0,
    "r": 0.05,
    "sigma": 0.20,
    "mu": 0.08,
    "N": 365,
    "n_paths": 1000
}

STRATEGY_INFO = {
    "Iron Condor": {
        "description": "Profit from low volatility. Sell both a put spread and call spread.",
        "strikes": ["K1", "K2", "K3", "K4"],
        "max_profit": "Premium collected",
        "max_loss": "K2-K1 or K4-K3"
    },
    "Straddle": {
        "description": "Profit from high volatility in either direction. Buy call + put at same strike.",
        "strikes": ["K1"],
        "max_profit": "Unlimited",
        "max_loss": "Premium paid"
    },
    "Strangle": {
        "description": "Similar to straddle but cheaper. Buy OTM put and OTM call.",
        "strikes": ["K1", "K2"],
        "max_profit": "Unlimited",
        "max_loss": "Premium paid"
    }
}

MODEL_DESCRIPTIONS = {
    "CRR": "Cox-Ross-Rubinstein: Standard exponential tree model",
    "Steve Shreve": "Linear approximation with symmetric probabilities",
    "Drift-Adjusted": "Incorporates real-world drift (μ) in tree construction"
}
