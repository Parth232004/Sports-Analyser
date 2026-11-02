
import pandas as pd
from analytics import validate_data

# Create valid sample football data
data = {
    "match": ["Match 1", "Match 1"],
    "team": ["City United", "Harbour FC"],
    "player": ["Dev Mehta", "Aarav Shah"],
    "shots": [5, 4],
    "shots_on_target": [3, 2],
    "goals": [2, 1],
    "passes": [30, 25],
    "successful_passes": [25, 20]
}

df = pd.DataFrame(data)

# Test 1: Valid dataset
valid, message = validate_data(df)
print("Test 1 - Valid dataset:", valid, message)

# Test 2: Invalid shots
invalid_df = df.copy()
invalid_df.loc[0, "shots_on_target"] = 10
valid, message = validate_data(invalid_df)
print("Test 2 - Invalid shots:", valid, message)

# Test 3: Negative values
negative_df = df.copy()
negative_df.loc[0, "goals"] = -1
valid, message = validate_data(negative_df)
print("Test 3 - Negative values:", valid, message)

# Test 4: Decimal values
decimal_df = df.copy()
decimal_df["shots"] = decimal_df["shots"].astype(float)
decimal_df.loc[0, "shots"] = 2.5
valid, message = validate_data(decimal_df)
print("Test 4 - Decimal values:", valid, message)

# Test 5: Duplicate players
duplicate_df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
valid, message = validate_data(duplicate_df)
print("Test 5 - Duplicate players:", valid, message)

# Test 6: Missing required column
missing_column_df = df.drop(columns=["goals"])

valid, message = validate_data(missing_column_df)
print("Test 6 - Missing column:", valid, message)


# Test 7: Blank player name
blank_player_df = df.copy()
blank_player_df.loc[0, "player"] = "   "

valid, message = validate_data(blank_player_df)
print("Test 7 - Blank player:", valid, message)
