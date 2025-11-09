import pytest
import numpy as np
from src.payouts import IronCondorPayout


class TestIronCondorPayout:
    
    def test_initialization_valid(self):
        """Valid strike ordering should initialize successfully."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        assert ic.K1 == 90
        assert ic.K2 == 95
        assert ic.K3 == 105
        assert ic.K4 == 110
    
    def test_initialization_invalid_ordering(self):
        """Invalid strike ordering should raise ValueError."""
        with pytest.raises(ValueError):
            IronCondorPayout(K1=95, K2=90, K3=105, K4=110)
        
        with pytest.raises(ValueError):
            IronCondorPayout(K1=90, K2=95, K3=100, K4=100)
    
    def test_payout_below_k1(self):
        """Price far below K1 should give max loss on put spread."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        final_prices = np.array([80, 85, 89])
        payouts = ic.calculate_payout(final_prices)
        
        expected = np.array([5, 5, 5])  # K2 - K1 = 95 - 90
        np.testing.assert_array_equal(payouts, expected)
    
    def test_payout_between_k1_k2(self):
        """Price between K1 and K2 should give partial put spread loss."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        final_prices = np.array([91, 93, 94])
        payouts = ic.calculate_payout(final_prices)
        
        expected = np.array([4, 2, 1])  # K2 - S
        np.testing.assert_array_equal(payouts, expected)
    
    def test_payout_profit_zone(self):
        """Price in profit zone (K2 to K3) should give zero payout."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        final_prices = np.array([95, 100, 105])
        payouts = ic.calculate_payout(final_prices)
        
        expected = np.array([0, 0, 0])
        np.testing.assert_array_equal(payouts, expected)
    
    def test_payout_between_k3_k4(self):
        """Price between K3 and K4 should give partial call spread loss."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        final_prices = np.array([106, 108, 109])
        payouts = ic.calculate_payout(final_prices)
        
        expected = np.array([1, 3, 4])  # S - K3
        np.testing.assert_array_equal(payouts, expected)
    
    def test_payout_above_k4(self):
        """Price far above K4 should give max loss on call spread."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        final_prices = np.array([111, 115, 120])
        payouts = ic.calculate_payout(final_prices)
        
        expected = np.array([5, 5, 5])  # K4 - K3 = 110 - 105
        np.testing.assert_array_equal(payouts, expected)
    
    def test_payout_all_zones(self):
        """Test payout across all zones simultaneously."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        final_prices = np.array([85, 92, 100, 107, 115])
        payouts = ic.calculate_payout(final_prices)
        
        expected = np.array([5, 3, 0, 2, 5])
        np.testing.assert_array_equal(payouts, expected)
    
    def test_accepts_list_input(self):
        """Should accept list input and convert to array."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        final_prices = [85, 100, 115]
        payouts = ic.calculate_payout(final_prices)
        
        assert isinstance(payouts, np.ndarray)
        expected = np.array([5, 0, 5])
        np.testing.assert_array_equal(payouts, expected)
    
    def test_exact_strike_boundaries(self):
        """Test exact strike price boundaries."""
        ic = IronCondorPayout(K1=90, K2=95, K3=105, K4=110)
        final_prices = np.array([90, 95, 105, 110])
        payouts = ic.calculate_payout(final_prices)
        
        # K1=90: in [K1, K2), payout = K2-S = 95-90 = 5
        # K2=95: in [K2, K3), payout = 0
        # K3=105: in [K3, K4), payout = S-K3 = 105-105 = 0
        # K4=110: in [K4, inf), payout = K4-K3 = 5
        expected = np.array([5, 0, 0, 5])
        np.testing.assert_array_equal(payouts, expected)
