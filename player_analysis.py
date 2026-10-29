
import pandas as pd

# Load the football dataset
df = pd.read_csv("data/football_stats.csv")

# Group statistics by player and team
players = df.groupby(
    ["team", "player"], as_index=False
).agg(
    total_goals=("goals", "sum"),
    total_shots=("shots", "sum"),
    shots_on_target=("shots_on_target", "sum"),
    total_passes=("passes", "sum"),
    successful_passes=("successful_passes", "sum")
)

# Calculate player-level accuracy
players["shooting_accuracy"] = (
    100 * players["shots_on_target"]
    / players["total_shots"].replace(0, float("nan"))
)

players["passing_accuracy"] = (
    100 * players["successful_passes"]
    / players["total_passes"].replace(0, float("nan"))
)

# Sort players by goals
players = players.sort_values(
    by="total_goals", ascending=False
)

# Display the results
print("\nPLAYER PERFORMANCE REPORT")
print(
    players[
        [
            "team",
            "player",
            "total_goals",
            "total_shots",
            "shooting_accuracy",
            "total_passes",
            "passing_accuracy"
        ]
    ].round(1).to_string(index=False)
)
