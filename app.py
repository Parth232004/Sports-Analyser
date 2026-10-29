from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Football Match Performance Analyzer", layout="wide")

from analytics import REQUIRED, NUMERIC, validate_data, add_metrics, build_insights

st.title("⚽ Football Match Performance Analyzer")
st.write("Upload match statistics to explore team and player performance.")
st.caption("Educational portfolio project. Automated observations are descriptive, not coaching diagnoses.")

default_path = Path(__file__).parent / "data" / "football_stats.csv"
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Could not read the CSV file: {exc}")
        st.stop()
else:
    raw = pd.read_csv(default_path)
    st.info("Showing the included illustrative sample dataset. Upload your own CSV to replace it.")

df = raw.copy()
valid, message = validate_data(df)
if not valid:
    st.error(message)
    st.stop()

df = add_metrics(df)
st.success(message)

matches = ["All matches"] + sorted(df["match"].astype(str).unique().tolist())
selected_match = st.selectbox("Match", matches)
if selected_match != "All matches":
    df = df[df["match"].astype(str) == selected_match]

teams = ["All teams"] + sorted(df["team"].astype(str).unique().tolist())
selected_team = st.selectbox("Team", teams)
if selected_team != "All teams":
    df = df[df["team"].astype(str) == selected_team]

goals = int(df["goals"].sum())
shots = int(df["shots"].sum())
on_target = int(df["shots_on_target"].sum())
passes = int(df["passes"].sum())
completed = int(df["successful_passes"].sum())


k1, k2, k3 = st.columns(3)
k1.metric("Goals", goals)
k2.metric("Total Shots", shots)
k3.metric("Shots on Target", on_target)

k4, k5, k6 = st.columns(3)
k4.metric("Shooting Accuracy", f"{on_target / shots * 100:.1f}%" if shots else "N/A")
k5.metric("Total Passes", passes)
k6.metric("Successful Passes", completed)

st.metric(
    "Passing Accuracy",
    f"{completed / passes * 100:.1f}%" if passes else "N/A"
)


team_stats = df.groupby("team", as_index=False).agg(
    goals=("goals", "sum"),
    shots=("shots", "sum"),
    shots_on_target=("shots_on_target", "sum"),
    passes=("passes", "sum"),
    successful_passes=("successful_passes", "sum")
)
team_stats["shot_accuracy_pct"] = (
    100 * team_stats["shots_on_target"] /
    team_stats["shots"].replace(0, float("nan"))
)
team_stats["pass_accuracy_pct"] = (
    100 * team_stats["successful_passes"] /
    team_stats["passes"].replace(0, float("nan"))
)

# Day 4: Team Performance Comparison
st.subheader("Team Performance Comparison")

team_report = team_stats.rename(columns={
    "team": "Team",
    "goals": "Goals",
    "shots": "Total Shots",
    "shots_on_target": "Shots on Target",
    "passes": "Total Passes",
    "successful_passes": "Successful Passes",
    "shot_accuracy_pct": "Shooting Accuracy (%)",
    "pass_accuracy_pct": "Passing Accuracy (%)",
})

st.dataframe(
    team_report.round(1),
    use_container_width=True,
    hide_index=True,
)


# Day 4: Compare goals scored by each team
st.subheader("Team Goals Comparison")

if not team_stats.empty:
    team_goals_chart = px.bar(
        team_stats,
        x="team",
        y="goals",
        color="team",
        title="Goals Scored by Team",
        labels={
            "team": "Team",
            "goals": "Total Goals",
        },
        text="goals",
    )

    team_goals_chart.update_layout(
        xaxis_title="Team",
        yaxis_title="Goals Scored",
        showlegend=False,
    )

    st.plotly_chart(
        team_goals_chart,
        use_container_width=True,
    )
else:
    st.info("No team data is available for the selected filters.")

# Day 4: Team Performance Insights
st.subheader("Team Performance Insights")

if team_stats.empty:
    st.info("No team insights are available for the selected filters.")
else:
    # Team with the most goals
    highest_goals = team_stats["goals"].max()
    goal_leaders = team_stats.loc[
        team_stats["goals"] == highest_goals, "team"
    ].tolist()

    if len(goal_leaders) == 1:
        st.write(
            f"- **Most goals:** {goal_leaders[0]} "
            f"scored {int(highest_goals)} goal(s)."
        )
    else:
        st.write(
            f"- **Most goals:** Teams tied at "
            f"{int(highest_goals)} goal(s): "
            f"{', '.join(goal_leaders)}."
        )

    # Team with the highest shooting accuracy
    shooting_data = team_stats.dropna(
        subset=["shot_accuracy_pct"]
    )

    if not shooting_data.empty:
        best_shooting = shooting_data.loc[
            shooting_data["shot_accuracy_pct"].idxmax()
        ]

        st.write(
            f"- **Highest shooting accuracy:** "
            f"{best_shooting['team']} "
            f"({best_shooting['shot_accuracy_pct']:.1f}%)."
        )

    # Team with the highest passing accuracy
    passing_data = team_stats.dropna(
        subset=["pass_accuracy_pct"]
    )

    if not passing_data.empty:
        best_passing = passing_data.loc[
            passing_data["pass_accuracy_pct"].idxmax()
        ]

        st.write(
            f"- **Highest passing accuracy:** "
            f"{best_passing['team']} "
            f"({best_passing['pass_accuracy_pct']:.1f}%)."
        )


# Prepare player statistics for charts
chart_stats = df.groupby(
    ["team", "player"], as_index=False
).agg(
    goals=("goals", "sum"),
    shots=("shots", "sum"),
    shots_on_target=("shots_on_target", "sum"),
)

chart_stats["shooting_accuracy_pct"] = (
    100 * chart_stats["shots_on_target"]
    / chart_stats["shots"].replace(0, float("nan"))
)

# Chart 1: Goals by player
st.subheader("Goals by Player")
fig1 = px.bar(
    chart_stats,
    x="player",
    y="goals",
    color="team",
    title="Goals Scored by Each Player",
)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Shots versus goals
st.subheader("Shots vs Goals")
fig2 = px.scatter(
    chart_stats,
    x="shots",
    y="goals",
    color="team",
    hover_name="player",
    title="Shots Compared with Goals",
)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Shooting accuracy
st.subheader("Shooting Accuracy by Player")
fig3 = px.bar(
    chart_stats,
    x="player",
    y="shooting_accuracy_pct",
    color="team",
    title="Shooting Accuracy (%)",
)
st.plotly_chart(fig3, use_container_width=True)



st.subheader("Player Performance Report")

# Combine statistics for each player within the selected filters
player_stats = df.groupby(
    ["team", "player"], as_index=False
).agg(
    matches=("match", "nunique"),
    goals=("goals", "sum"),
    total_shots=("shots", "sum"),
    shots_on_target=("shots_on_target", "sum"),
    total_passes=("passes", "sum"),
    successful_passes=("successful_passes", "sum"),
)

# Calculate accuracy from combined totals
player_stats["shooting_accuracy_pct"] = (
    100 * player_stats["shots_on_target"]
    / player_stats["total_shots"].replace(0, float("nan"))
)

player_stats["passing_accuracy_pct"] = (
    100 * player_stats["successful_passes"]
    / player_stats["total_passes"].replace(0, float("nan"))
)

# Display the most prolific goal scorers first
player_stats = player_stats.sort_values(
    ["goals", "total_shots"],
    ascending=[False, False]
)

# Show accuracy to one decimal place
st.dataframe(
    player_stats.round(1),
    use_container_width=True,
    hide_index=True
)


st.subheader("Automated match insights")
for insight in build_insights(df):
    st.write(f"- {insight}")

st.download_button(
    "Download filtered statistics",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="football_analysis.csv",
    mime="text/csv"
)
