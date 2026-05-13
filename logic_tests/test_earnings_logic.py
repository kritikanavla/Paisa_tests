import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add Paisa server to path
SERVER_PATH = os.environ.get("PAISA_SERVER_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "paisa", "server"))
if SERVER_PATH not in sys.path:
    sys.path.append(SERVER_PATH)

from services.strategy.arbiter import select_strategy_candidates

@pytest.mark.anyio
async def test_earnings_blackout_logic():
    """Verify that premium-selling is blocked during the 14-day earnings window."""
    
    # 1. SETUP: 5 days to earnings (Within 14-day blackout)
    ticker = "AAPL"
    days_to_earnings = 5
    paisa_score = 80
    volatility_rank = 20
    current_price = 200.0
    
    # Allowed strategies including Spreads (Premium Selling) and LEAPS (Buying)
    config = {
        "allowed_strategies": ["SPREAD", "LEAPS", "LONG_STOCK"],
        "max_vix": 30.0
    }
    
    # Mock skill_service to return default logic
    with patch("services.agents.skill_service.skill_service.get_skill_logic") as mock_logic:
        mock_logic.return_value = {"earnings_blackout_days": 14}
        
        candidates = await select_strategy_candidates(
            ticker, current_price, paisa_score, volatility_rank, 
            vwap=200, rvol=1.0, technical_signals=[], 
            bypass_score_filter=False, vix=15.0, 
            days_to_earnings=days_to_earnings, config=config
        )
        
        # 2. VERIFY: 'SPREAD' (Premium) should be BLOCKED, but 'LEAPS' (Buying) should be ALLOWED
        strategy_types = [c["strategy_type"] for c in candidates]
        
        assert "LEAPS" in strategy_types
        assert "SPREAD" not in strategy_types
        print("DEBUG: SPREAD correctly blocked during earnings blackout.")

@pytest.mark.anyio
async def test_crush_mode_iron_condor_gap():
    """Check if 'Crush Mode' (Iron Condors) is implemented for <2 days to earnings."""
    
    # 2 days to earnings -> Whitepaper says should be Iron Condor
    ticker = "AAPL"
    days_to_earnings = 2
    
    config = {
        "allowed_strategies": ["IRON_CONDOR", "SPREAD"],
        "max_vix": 30.0
    }
    
    with patch("services.agents.skill_service.skill_service.get_skill_logic") as mock_logic:
        mock_logic.return_value = {"earnings_blackout_days": 14}
        
        candidates = await select_strategy_candidates(
            ticker, 200.0, 80, 20, 200, 1.0, [], False, 15.0, 
            days_to_earnings=days_to_earnings, config=config
        )
        
        # 3. VERIFY: Does Iron Condor appear? 
        # (Based on audit, this is likely a GAP)
        strategy_types = [c["strategy_type"] for c in candidates]
        
        if "IRON_CONDOR" not in strategy_types:
            pytest.fail("GAP FOUND: 'Crush Mode' Iron Condor not implemented for near-earnings events.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_earnings_blackout_logic())
    print("Earnings logic tests passed!")
