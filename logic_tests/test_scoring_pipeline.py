import sys
import os
import pytest
import asyncio
from unittest.mock import MagicMock, patch

# Add Paisa server to path
SERVER_PATH = os.environ.get("PAISA_SERVER_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "paisa", "server"))
if SERVER_PATH not in sys.path:
    sys.path.append(SERVER_PATH)

from services.strategy.scoring_pipeline import ScoringPipeline, ScoringContext, RegimePenaltyStage, RuleEvaluationStage
from core.models import Methodology, Rule

@pytest.mark.anyio
async def test_regime_penalty_logic():
    """Verify that Bear Market Regime adds a -30 penalty metadata."""
    
    # Mock Market Data to return Bear Regime
    with patch("services.market.market_data.get_market_regime") as mock_regime:
        mock_regime.return_value = {"safe": False, "bullish_off": True}
        
        # Mock methodology with a simple rule
        methodology = Methodology(name="Test Methodology", sector="Technology", rules=[
            Rule(metric="operatingMargins", operator=">", value=0.1, weight=50)
        ])
        
        company_data = {
            "ticker": "AAPL",
            "sector": "Technology",
            "financials": {"operatingMargins": 0.2},
            "technicals": {}
        }
        
        context = ScoringContext(company_data, methodology, {})
        stages = [
            RegimePenaltyStage(),
            RuleEvaluationStage()
        ]
        pipeline = ScoringPipeline(stages)
        
        result = await pipeline.run(context)
        
        # In v2.6, regime penalty is metadata, now in score_details (PAISA-13)
        assert result["score_details"]["regime_penalty"] == -30
        assert result["score"] == 100.0 # Score is now the final rating

@pytest.mark.anyio
async def test_metric_fallback_logic():
    """Verify that SMA fallbacks work if priceVs50DayMA is missing."""
    
    methodology = Methodology(name="Test Methodology", sector="Technology", rules=[
        Rule(metric="priceVs50DayMA", operator="==", value=1.0, weight=50)
    ])
    
    # Missing priceVs50DayMA but has currentPrice and sma_50
    company_data = {
        "ticker": "AAPL",
        "sector": "Technology",
        "financials": {
            "currentPrice": 160.0,
            "sma_50": 150.0
        },
        "technicals": {}
    }
    
    context = ScoringContext(company_data, methodology, {})
    stages = [RuleEvaluationStage()]
    pipeline = ScoringPipeline(stages)
    
    result = await pipeline.run(context)
    
    # Should pass because 160 > 150 -> metric_value becomes 1.0
    # PAISA-13: score is now percentage
    assert result["score"] == 100.0 
    assert result["score_details"]["raw_points"] == 50.0
    assert result["rules_applied"][0]["passed"] is True

if __name__ == "__main__":
    asyncio.run(test_regime_penalty_logic())
    asyncio.run(test_metric_fallback_logic())
