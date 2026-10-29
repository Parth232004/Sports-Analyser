import pandas as pd

# Load football data
df = pd.read_csv("data/football_stats.csv")

# Calculate shots
total_shots = df["shots"].sum()
shots_on_target = df["shots_on_target"].sum()

# Calculate passes
total_passes = df["passes"].sum()
successful_passes = df["successful_passes"].sum()

# Calculate accuracy
shooting_accuracy = shots_on_target / total_shots * 100
passing_accuracy = successful_passes / total_passes * 100

# Print results
print("Total shots:", total_shots)
print("Shots on target:", shots_on_target)
print("Shooting accuracy:", round(shooting_accuracy, 1), "%")

print("Total passes:", total_passes)
print("Successful passes:", successful_passes)
print("Passing accuracy:", round(passing_accuracy, 1), "%")