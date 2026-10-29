# Seven-Day Learning Roadmap

Daily time: 2–3 hours. Keep the scope small and finish a working version before adding extras.

## Day 1 — Setup and data (2–3 hours)
- Install Python environment and dependencies.
- Open `data/football_stats.csv` and understand every column.
- Learn rows, columns, data types, missing values, and `read_csv`.
- Deliverable: app runs with the supplied sample data.

## Day 2 — Football KPIs (2–3 hours)
- Calculate shooting accuracy = shots on target / shots × 100.
- Calculate passing accuracy = successful passes / passes × 100.
- Explain why totals and percentages can tell different stories.
- Deliverable: explain the KPI formulas in your own words.

## Day 3 — Charts and comparisons (2–3 hours)
- Explore the team goals bar chart and shots-goals scatter plot.
- Change the chart types or labels.
- Compare teams without making claims beyond the data.
- Deliverable: two charts you can explain.

## Day 4 — Data validation and insights (2–3 hours)
- Read `validate_data` and `build_insights` in `app.py`.
- Test missing columns, negative values, and impossible counts.
- Change the rule-based insight threshold and explain your choice.
- Deliverable: valid input checks and understandable observations.

## Day 5 — Streamlit interface (2–3 hours)
- Explore the match/team filters, KPI cards, table, and download button.
- Add one feature, such as a player selector or a match summary.
- Deliverable: usable interactive dashboard.

## Day 6 — Testing and data research (2–3 hours)
- Run `pytest -q`.
- Fix any issues you discover.
- If using real data, verify source, license, schema, and attribution.
- Deliverable: tests pass and dataset source is documented.

## Day 7 — GitHub portfolio (2–3 hours)
- Create a GitHub repository and push source files.
- Add a dashboard screenshot and your key findings to README.
- Record a short demo if possible.
- Deliverable: repository link ready to add to your resume.

## Stretch goal only if the core app is complete
Use real shot-level event data to train a small classifier. Define the prediction target, split train/test before fitting transformations, choose suitable metrics, and compare against a simple baseline. Do not claim machine learning if you have not trained and evaluated a model.
