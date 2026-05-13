import sys
import os
import pytest
from datetime import datetime, timedelta

# Add Paisa server to path
SERVER_PATH = os.environ.get("PAISA_SERVER_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "paisa", "server"))
if SERVER_PATH not in sys.path:
    sys.path.append(SERVER_PATH)

from services.strategy.strategies_utils.management import check_exit_conditions

def test_atr_stop_loss():
    """Verify that a 2x ATR drop triggers an exit."""
    trade_data = {
        "ticker": "AAPL",
        "entry_price_stock": 150.0,
        "highest_stock_price": 155.0,
        "atr_at_entry": 2.0, # 2x ATR = 4.0
        "entry_price_option": 5.0,
        "strategy": "LEAPS",
        "strategy_side": 1,
        "trade_type": "OPTION"
    }
    
    # 1. Price at 152 (Drop of 3 from peak, < 4) -> No exit
    triggered, reason = check_exit_conditions(trade_data, 152.0, 6.0, datetime.now())
    assert not triggered
    
    # 2. Price at 150.5 (Drop of 4.5 from peak, > 4) -> EXIT
    triggered, reason = check_exit_conditions(trade_data, 150.5, 4.0, datetime.now())
    assert triggered
    assert "ATR" in reason

def test_21_dte_gamma_risk():
    """Verify that short options are closed at 21 DTE."""
    now = datetime.now()
    expiry_25_days = now + timedelta(days=25)
    expiry_20_days = now + timedelta(days=20)
    
    trade_data = {
        "strategy": "BULL_PUT_SPREAD",
        "strategy_side": -1, # Short
        "trade_type": "OPTION",
        "entry_price_option": 1.0,
        "expiry_date": expiry_25_days.isoformat(),
        "days_held": 0
    }
    
    # 1. 25 DTE -> No exit (Price at 0.9 means 10% profit, below 50% TP)
    triggered, reason = check_exit_conditions(trade_data, 100.0, 0.9, now)
    if triggered:
        print(f"DEBUG: 25 DTE Triggered unexpectedly. Reason: {reason}")
    assert not triggered
    
    # 2. 20 DTE -> EXIT
    trade_data["expiry_date"] = expiry_20_days.isoformat()
    triggered, reason = check_exit_conditions(trade_data, 100.0, 0.5, now)
    assert triggered
    assert "21 DTE GAMMA RISK" in reason

def test_trailing_stop_lock_5_percent():
    """Verify that a 20% gain followed by a drop to 5% locks the yield."""
    trade_data = {
        "strategy": "LONG_STOCK",
        "strategy_side": 1,
        "trade_type": "STOCK",
        "entry_price_option": 100.0,
        "highest_profit_pct": 0.25, # Was at 25% profit
        "quantity": 100,
        "contract_multiplier": 1
    }
    
    # 1. Current profit at 10% -> No exit (but below 25% peak)
    triggered, reason = check_exit_conditions(trade_data, 110.0, 110.0, datetime.now())
    assert not triggered
    
    # 2. Current profit at 4% -> EXIT (Locks 5% yield requirement)
    # Note: The logic says profit_pct <= 0.05
    triggered, reason = check_exit_conditions(trade_data, 104.0, 104.0, datetime.now())
    assert triggered
    assert "TRAILING STOP (LOCK 5%)" in reason

def test_long_leaps_delta_decay():
    """Verify that LEAPS are closed if delta drops below 0.50."""
    # We'll need to mock calculate_black_scholes_delta or use a strike where delta is low
    # For now, let's just ensure the logic path exists
    # If delta is < 0.50 -> EXIT
    
    # This requires mocking the greeks service or providing realistic parameters
    pass

if __name__ == "__main__":
    pytest.main([__file__])
