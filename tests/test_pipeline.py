import pytest
from app.agents.pipeline import run_pipeline, RISK_THRESHOLD, TX_COUNT_CAP, VOLUME_XLM_CAP
@pytest.mark.parametrize(
    "count,volume,score,activity,volume_score,level,exceeded",
    [
        (0, 0, 0, 0.0, 0.0, "low", False),
        (100, 0, 60, 60.0, 0.0, "elevated", False),
        (0, 1_000_000, 40, 0.0, 40.0, "elevated", False),
        (101, 1_000_001, 100, 60.0, 40.0, "high", True),
        (1000, 10_000_000, 100, 60.0, 40.0, "high", True),
        (50, 250_000, 40, 30.0, 10.0, "elevated", False),
        (50, 225_000, 39, 30.0, 9.0, "low", False),
        (50, 275_000, 41, 30.0, 11.0, "elevated", False),
        (100, 225_000, 69, 60.0, 9.0, "elevated", False),
        (100, 250_000, 70, 60.0, 10.0, "high", True),
        (100, 275_000, 71, 60.0, 11.0, "high", True),
    ],
)
def test_pipeline_contract(count, volume, score, activity, volume_score, level, exceeded):
    result = run_pipeline("synthetic-account", count, volume)
    assert result["address"] == "synthetic-account"
    assert result["score"] == score
    assert result["score_breakdown"] == {
        "transaction_activity": activity,
        "transaction_volume": volume_score,
    }
    assert result["risk_level"] == level
    assert result["threshold_exceeded"] is exceeded
    assert result["threshold"] == 70
    assert result["on_chain_action"] == "none"
def test_documented_threshold_is_stable():
    assert RISK_THRESHOLD == 70
    assert TX_COUNT_CAP == 100
    assert VOLUME_XLM_CAP == 1_000_000
