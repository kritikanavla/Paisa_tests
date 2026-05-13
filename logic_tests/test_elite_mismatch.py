import sys
import os
import pytest

# Add Paisa server to path
SERVER_PATH = os.environ.get("PAISA_SERVER_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "paisa", "server"))
if SERVER_PATH not in sys.path:
    sys.path.append(SERVER_PATH)

from services.strategy.scoring import detect_elite_mismatch

def test_elite_mismatch_trigger():
    """Verify that Elite Mismatch triggers on high AI vs low Quant."""
    
    # High AI (80) vs Low Paisa (40) -> Should trigger
    company_data = {
        "financials": {
            "metricsScore": 80,
            "contextScore": 20
        }
    }
    score_data = {"percentage": 40.0}
    
    assert detect_elite_mismatch(company_data, score_data) is True

def test_elite_mismatch_35_point_gap():
    """Verify that a 35+ point gap triggers the mismatch flag."""
    
    # Gap of 35 points exactly
    company_data = {
        "financials": {
            "metricsScore": 70,
            "contextScore": 70
        }
    }
    score_data = {"percentage": 35.0}
    
    assert detect_elite_mismatch(company_data, score_data) is True

def test_elite_mismatch_both_high_no_trigger():
    """Verify that if both are high, no mismatch is triggered (agreement)."""
    
    # Both >= 70 -> No mismatch
    company_data = {
        "financials": {
            "metricsScore": 75,
            "contextScore": 75
        }
    }
    score_data = {"percentage": 70.0}
    
    assert detect_elite_mismatch(company_data, score_data) is False

if __name__ == "__main__":
    test_elite_mismatch_trigger()
    test_elite_mismatch_35_point_gap()
    test_elite_mismatch_both_high_no_trigger()
    print("Elite Mismatch tests passed!")
