import pandas as pd
from analytics import add_metrics, build_insights, validate_data

def sample():
    return pd.DataFrame([{
        "match": "M1", "team": "A", "player": "P1",
        "shots": 4, "shots_on_target": 2, "goals": 1,
        "passes": 10, "successful_passes": 8
    }])

def test_valid_sample():
    df = sample()
    valid, _ = validate_data(df)
    assert valid

def test_metric_calculations():
    df = add_metrics(sample())
    assert df.loc[0, "shot_accuracy_pct"] == 50
    assert df.loc[0, "pass_accuracy_pct"] == 80

def test_invalid_shots_on_target():
    df = sample()
    df.loc[0, "shots_on_target"] = 5
    valid, message = validate_data(df)
    assert not valid
    assert "Shots on target" in message

def test_insights_created():
    messages = build_insights(sample())
    assert len(messages) >= 3
