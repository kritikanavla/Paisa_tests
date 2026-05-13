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
async def test_vrp_vol_rank_gating():
    """Verify that high volatility rank gates buying leverage (ZEBRA/LEAPS)."""
    
    # 1. SETUP: High Volatility Rank (60)
    ticker = "AAPL"
    paisa_score = 90
    volatility_rank = 60
    current_price = 200.0
    
    config = {
        "allowed_strategies": ["ZEBRA", "LEAPS", "SPREAD"],
        "max_vix": 40.0
    }
    
    with patch("services.agents.skill_service.skill_service.get_skill_logic") as mock_logic:
        mock_logic.return_value = {}
        
        candidates = await select_strategy_candidates(
            ticker, current_price, paisa_score, volatility_rank, 
            vwap=200, rvol=1.0, technical_signals=[], 
            bypass_score_filter=False, vix=15.0, 
            days_to_earnings=99, config=config
        )
        
        strategy_types = [c["strategy_type"] for c in candidates]
        
        # 2. VERIFY: 'ZEBRA' should be BLOCKED (needs < 45)
        # 'LEAPS' might be blocked depending on the implementation in bullish.py
        
        assert "ZEBRA" not in strategy_types, "ZEBRA should be gated by high volatility rank (>45)"
        print("DEBUG: ZEBRA correctly gated by High Volatility.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_vrp_vol_rank_gating())
    print("VRP gating tests passed!")
