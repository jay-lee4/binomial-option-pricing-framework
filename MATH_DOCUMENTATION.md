# Mathematical Documentation

## Binomial Tree Models

### Cox-Ross-Rubinstein (CRR) Model

#### Parameters
- **Up factor**: `u = e^(σ√Δt)`
- **Down factor**: `d = 1/u = e^(-σ√Δt)`
- **Risk-neutral probability**: `q = (e^(rΔt) - d) / (u - d)`
- **Time step**: `Δt = T/N`

#### Stock Price Evolution
At node (n, j) where n is time step and j is number of up moves:
```
S(n,j) = S₀ * u^j * d^(n-j)
```

#### Option Valuation
Backward induction from terminal nodes:
```
V(n,j) = e^(-rΔt) * [q * V(n+1,j+1) + (1-q) * V(n+1,j)]
```

For European options at terminal nodes:
```
Call: max(S(N,j) - K, 0)
Put:  max(K - S(N,j), 0)
```

---

### Steve Shreve Model

#### Parameters
- **Up factor**: `u = e^((r - σ²/2)Δt + σ√Δt)`
- **Down factor**: `d = e^((r - σ²/2)Δt - σ√Δt)`
- **Risk-neutral probability**: `q = (e^(rΔt) - d) / (u - d)`

This model has drift incorporated into the up/down factors rather than the probability.

#### Key Property
Unlike CRR, ud ≠ 1 in the Shreve model.

---

### Drift-Adjusted Model

#### Parameters
- **Up factor**: `u = e^(σ√Δt)`
- **Down factor**: `d = 1/u`
- **Real-world probability**: `p = (e^(μΔt) - d) / (u - d)`

Uses expected return μ instead of risk-free rate r.

#### Important Note
This model is NOT risk-neutral and does NOT give arbitrage-free prices. It's used for P-measure analysis.

---

## Geometric Brownian Motion (GBM)

### Continuous Process
```
dS = μS dt + σS dW
```

Where:
- μ: drift (expected return)
- σ: volatility
- dW: Wiener process increment

### Discrete Simulation
```
S(t+Δt) = S(t) * e^((μ - σ²/2)Δt + σ√Δt * Z)
```

Where Z ~ N(0,1) is a standard normal random variable.

### Expected Value
```
E[S(T)] = S₀ * e^(μT)
```

### Variance
```
Var[S(T)] = S₀² * e^(2μT) * (e^(σ²T) - 1)
```

---

## Iron Condor Payoff

### Structure
- Buy put at K₁
- Sell put at K₂
- Sell call at K₃
- Buy call at K₄

### Payoff at Expiration
```
Payoff = max(K₁ - Sᴛ, 0) - max(K₂ - Sᴛ, 0) - max(Sᴛ - K₃, 0) + max(Sᴛ - K₄, 0)
```

### Simplified by Region
- **Sᴛ < K₁**: Payoff = K₁ - K₂ (max loss on put side)
- **K₁ ≤ Sᴛ < K₂**: Payoff = K₂ - Sᴛ
- **K₂ ≤ Sᴛ ≤ K₃**: Payoff = 0 (profit = premium)
- **K₃ < Sᴛ ≤ K₄**: Payoff = Sᴛ - K₃
- **Sᴛ > K₄**: Payoff = K₃ - K₄ (max loss on call side)

### Profit/Loss
```
P/L = Initial Premium - |Payoff|
```

---

## Probability Calculations

### Risk-Neutral Probability (Q-Measure)

At terminal node with j up moves:
```
Q(j) = C(N,j) * q^j * (1-q)^(N-j)
```

Where C(N,j) is the binomial coefficient.

### Real-World Probability (P-Measure)
```
P(j) = C(N,j) * p^j * (1-p)^(N-j)
```

### Probability of Profit (Iron Condor)
```
P(profit) = Σ P(j) for all j where K₂ < S(N,j) < K₃
```

---

## Expected Value Calculations

### GBM Expected Profit
```
E[Profit]_GBM = Initial Premium - (1/M) * Σᵢ₌₁ᴹ Payoff(Sᴛ⁽ⁱ⁾)
```

Where M is the number of Monte Carlo paths.

### Real-World Expected Profit
```
E[Profit]_RW = Initial Premium - Σⱼ₌₀ᴺ P(j) * Payoff(S(N,j))
```

Using real-world probabilities P(j).

---

## Convergence Properties

### CRR Convergence to Black-Scholes
As N → ∞:
```
V_CRR → V_BS
```

Where V_BS is the Black-Scholes price.

### Rate of Convergence
The error decreases as O(1/N) for European options.

---

## Greeks (Not Yet Implemented)

### Delta (∂V/∂S)
```
Δ = (V(S+ΔS) - V(S-ΔS)) / (2ΔS)
```

### Gamma (∂²V/∂S²)
```
Γ = (V(S+ΔS) - 2V(S) + V(S-ΔS)) / (ΔS²)
```

### Theta (∂V/∂t)
```
Θ = (V(t+Δt) - V(t)) / Δt
```

### Vega (∂V/∂σ)
```
ν = (V(σ+Δσ) - V(σ-Δσ)) / (2Δσ)
```

---

## Optimization Objective

### Maximize Expected Profit
```
max E[Profit] = max (Initial Premium - E[Payoff])
```

Subject to:
- K₁ < K₂ < K₃ < K₄
- All prices positive
- Reasonable spreads

The optimizer searches over discrete grid of strike combinations.
```
