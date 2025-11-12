import numpy as np


class IronCondorPayout:
    """
    Iron Condor payout calculator.
    
    Structure: K1 < K2 < K3 < K4
    - Buy put at K1 (long put, lower strike)
    - Sell put at K2 (short put)
    - Sell call at K3 (short call)
    - Buy call at K4 (long call, higher strike)
    
    Max profit when K2 <= S <= K3 (price stays in middle range)
    Max loss when S <= K1 or S >= K4 (price moves far outside)
    """
    
    def __init__(self, K1: float, K2: float, K3: float, K4: float):
        if not (K1 < K2 < K3 < K4):
            raise ValueError(f"Strikes must satisfy K1 < K2 < K3 < K4, got {K1}, {K2}, {K3}, {K4}")
        
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.K4 = K4
    
    def calculate_payout(self, final_prices: np.ndarray) -> np.ndarray:
        if isinstance(final_prices, list):
            final_prices = np.array(final_prices)
        
        final_prices = np.asarray(final_prices)
        payouts = np.zeros_like(final_prices, dtype=float)
        
        mask_1 = final_prices < self.K1
        mask_2 = (self.K1 <= final_prices) & (final_prices < self.K2)
        mask_3 = (self.K2 <= final_prices) & (final_prices < self.K3)
        mask_4 = (self.K3 <= final_prices) & (final_prices < self.K4)
        mask_5 = final_prices >= self.K4
        
        payouts[mask_1] = self.K2 - self.K1
        payouts[mask_2] = self.K2 - final_prices[mask_2]
        payouts[mask_3] = 0
        payouts[mask_4] = final_prices[mask_4] - self.K3
        payouts[mask_5] = self.K4 - self.K3
        
        return payouts


class StraddlePayout:
    """
    Long Straddle payout calculator.
    
    Structure: Buy call + buy put at same strike K
    - Profits from large price movements in either direction
    - Max loss = premium paid (not calculated here, just intrinsic value)
    - Unlimited upside, large downside potential
    """
    
    def __init__(self, K: float):
        if K <= 0:
            raise ValueError(f"Strike K must be positive, got {K}")
        self.K = K
    
    def calculate_payout(self, final_prices: np.ndarray) -> np.ndarray:
        if isinstance(final_prices, list):
            final_prices = np.array(final_prices)
        
        final_prices = np.asarray(final_prices)
        
        call_payout = np.maximum(0, final_prices - self.K)
        put_payout = np.maximum(0, self.K - final_prices)
        
        return call_payout + put_payout


class StranglePayout:
    """
    Long Strangle payout calculator.
    
    Structure: K_put < K_call
    - Buy put at lower strike K_put
    - Buy call at higher strike K_call
    - Similar to straddle but cheaper, requires larger move to profit
    """
    
    def __init__(self, K_put: float, K_call: float):
        if K_put >= K_call:
            raise ValueError(f"Put strike must be less than call strike, got {K_put} >= {K_call}")
        if K_put <= 0 or K_call <= 0:
            raise ValueError(f"Strikes must be positive, got {K_put}, {K_call}")
        
        self.K_put = K_put
        self.K_call = K_call
    
    def calculate_payout(self, final_prices: np.ndarray) -> np.ndarray:
        if isinstance(final_prices, list):
            final_prices = np.array(final_prices)
        
        final_prices = np.asarray(final_prices)
        
        put_payout = np.maximum(0, self.K_put - final_prices)
        call_payout = np.maximum(0, final_prices - self.K_call)
        
        return put_payout + call_payout
