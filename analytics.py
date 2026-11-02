
import pandas as pd

REQUIRED = [
    "match", "team", "player", "shots", "shots_on_target",
    "goals", "passes", "successful_passes"
]

NUMERIC = [
    "shots", "shots_on_target", "goals",
    "passes", "successful_passes"
]


def validate_data(df: pd.DataFrame) -> tuple[bool, str]:
    """Validate required columns and basic football-stat constraints."""

    # 1. Check required columns
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}"

    # 2. Check blank text fields
    if df[["match", "team", "player"]].isna().any().any():
        return False, "Match, team, and player fields cannot be blank."

    for column in ["match", "team", "player"]:
        if df[column].astype(str).str.strip().eq("").any():
            return False, f"{column.capitalize()} fields cannot be blank."

    # 3. Convert statistics into numeric values
    numeric_data = df[NUMERIC].apply(pd.to_numeric, errors="coerce")

    if numeric_data.isna().any().any():
        return False, "Numeric statistics contain blank or non-numeric values."

    # 4. Reject negative values
    if (numeric_data < 0).any().any():
        return False, "Statistics cannot be negative."

    # 5. Reject decimal values
    if (numeric_data % 1 != 0).any().any():
        return False, "Football statistics must be whole numbers."

    # 6. Check football-stat constraints
    if (numeric_data["shots_on_target"] > numeric_data["shots"]).any():
        return False, "Shots on target cannot exceed total shots."

    if (numeric_data["goals"] > numeric_data["shots_on_target"]).any():
        return False, "For this simplified dataset, goals cannot exceed shots on target."

    if (numeric_data["successful_passes"] > numeric_data["passes"]).any():
        return False, "Successful passes cannot exceed total passes."

    # 7. Check duplicate player records
    duplicates = df.duplicated(
        subset=["match", "team", "player"], keep=False
    )

    if duplicates.any():
        return False, "Duplicate player records found for the same match and team."

    # 8. Update numeric columns
    df[NUMERIC] = numeric_data

    return True, "Data looks valid."


def add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate shooting and passing accuracy."""

    result = df.copy()

    result["shot_accuracy_pct"] = (
        100 * result["shots_on_target"] /
        result["shots"].replace(0, float("nan"))
    )

    result["pass_accuracy_pct"] = (
        100 * result["successful_passes"] /
        result["passes"].replace(0, float("nan"))
    )

    return result


def build_insights(df: pd.DataFrame) -> list[str]:
    """Create simple descriptive observations, not tactical certainty."""

    insights = []

    shots = int(df["shots"].sum())
    on_target = int(df["shots_on_target"].sum())
    passes = int(df["passes"].sum())
    completed = int(df["successful_passes"].sum())
    goals = int(df["goals"].sum())

    if shots:
        pct = on_target / shots * 100

        insights.append(
            f"{on_target} of {shots} shots were on target ({pct:.1f}%). "
            + (
                "Review shot selection and accuracy."
                if pct < 40
                else "More than 40% of recorded shots were on target."
            )
        )
    else:
        insights.append("No shots were recorded in this selection.")

    if passes:
        pct = completed / passes * 100

        insights.append(
            f"{completed} of {passes} passes were successful ({pct:.1f}%)."
        )
    else:
        insights.append("No passes were recorded in this selection.")

    insights.append(
        f"The selected data contains {goals} goals. "
        "Interpret this alongside opponent quality, game state, and match context."
    )

    return insights

