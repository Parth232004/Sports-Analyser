# Football Match Performance Analyzer

A beginner-friendly football analytics dashboard built with Python, Pandas, Plotly, and Streamlit.

## Features
- CSV upload and input validation
- Match and team filters
- Goals, shots, shooting accuracy, and passing accuracy KPIs
- Team performance comparison charts
- Player statistics and performance reports
- Player rankings based on goals, shooting accuracy, and passing accuracy
- Top goal scorer identification
- Best shooting and passing performer identification
- Match-wise performance summary
- Goals scored comparison across matches
- Rule-based descriptive match and player insights
- CSV export

## Important dataset note
The reusable calculations and validation functions are in `analytics.py`; tests import that module without
 launching the Streamlit interface.

## Technologies Used
- Python
- Pandas
- Plotly
- Streamlit

## Run locally (macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Run tests
```bash
python -m pip install pytest
pytest -q
```

The reusable calculations and validation functions are in `analytics.py`; tests import that module without
 launching the Streamlit interface.

## CSV format
Required columns:
`match, team, player, shots, shots_on_target, goals, passes, successful_passes`

Each row represents one player's aggregate statistics in one match.

## Project limitations
This version uses aggregate player statistics. It does not include event locations, shot coordinates, tactical heatmaps, xG, or a trained machine-learning model. Its insights are simple descriptive rules and should not be treated as definitive tactical advice.

## Future improvements
1. Import real event-level data with attribution and license compliance.
2. Add player-role comparisons and season trends.
3. Train and evaluate a model using shot-level data and a proper held-out test set.
4. Deploy the dashboard and add screenshots.
