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
        """
        Calculate payout at expiration for given final prices.
        
        Payout structure:
        - S < K1: payout = K2 - K1 (max loss on put spread)
        - K1 <= S < K2: payout = K2 - S (partial loss on put spread)
        - K2 <= S < K3: payout = 0 (max profit zone)
        - K3 <= S < K4: payout = S - K3 (partial loss on call spread)
        - S >= K4: payout = K4 - K3 (max loss on call spread)
        
        Args:
            final_prices: Array of final stock prices at expiration
            
        Returns:
            Array of payout values (what we owe, not profit)
        """
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
