import pandas as pd

REQUIRED = [
    "match", "team", "player", "shots", "shots_on_target",
    "goals", "passes", "successful_passes"
]
NUMERIC = ["shots", "shots_on_target", "goals", "passes", "successful_passes"]


def validate_data(df: pd.DataFrame) -> tuple[bool, str]:
    """Validate required columns and basic football-stat constraints."""
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}"

    df[NUMERIC] = df[NUMERIC].apply(pd.to_numeric, errors="coerce")
    if df[NUMERIC].isna().any().any():
        return False, "Numeric statistics contain blank or non-numeric values."
    if (df[NUMERIC] < 0).any().any():
        return False, "Statistics cannot be negative."
    if (df["shots_on_target"] > df["shots"]).any():
        return False, "Shots on target cannot exceed total shots."
    if (df["goals"] > df["shots_on_target"]).any():
        return False, "For this simplified dataset, goals cannot exceed shots on target."
    if (df["successful_passes"] > df["passes"]).any():
        return False, "Successful passes cannot exceed total passes."
    if df[["match", "team", "player"]].isna().any().any():
        return False, "Match, team, and player fields cannot be blank."
    return True, "Data looks valid."


def add_metrics(df: pd.DataFrame) -> pd.DataFrame:
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
            + ("Review shot selection and accuracy." if pct < 40
               else "More than 40% of recorded shots were on target.")
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
