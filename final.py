import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

"""
Variables & Units:
- time_spent_alone: Hours spent alone daily (0–11).
- stage_fear: Presence of stage fright (Yes/No).
- social_event_attendance: Frequency of social events (0–10).
- going_outside: Frequency of going outside (0–7).
- drained_after_socializing: Feeling drained after socializing (Yes/No).
- friends_circle_size: Number of close friends (0–15).
- post_frequency: Social media post frequency (0–10).
- personality: Target variable (Extrovert/Introvert).
"""

# 1. Load & clean data
df = pd.read_csv("personality_datasert.csv")
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Round numeric columns
numeric_cols = df.select_dtypes(include="number").columns
df[numeric_cols] = df[numeric_cols].round(1)

# Remove decimals from friends_circle_size
if "friends_circle_size" in df.columns:
    df["friends_circle_size"] = df["friends_circle_size"].round().astype(int)

# 2. Define colors & ordering
introvert_color       = "#ff9999"
extrovert_color       = "#66b3ff"
color_pair            = [introvert_color, extrovert_color]
ordered_personalities = ["Introvert", "Extrovert"]

# 3. Prepare pie-chart data
stage_fear_counts  = df["stage_fear"].value_counts().sort_index()
drain_counts       = df["drained_after_socializing"].value_counts().sort_index()
personality_counts = df["personality"].value_counts().sort_index()

# 4. Prepare stacked-bar data
stacked_alone   = df.groupby(["time_spent_alone",     "personality"]).size().unstack(fill_value=0)
stacked_social  = df.groupby(["social_event_attendance","personality"]).size().unstack(fill_value=0)
stacked_outside = df.groupby(["going_outside",        "personality"]).size().unstack(fill_value=0)
stacked_friends = df.groupby(["friends_circle_size",  "personality"]).size().unstack(fill_value=0)
stacked_post    = df.groupby(["post_frequency",       "personality"]).size().unstack(fill_value=0)

# 5. Plot dashboard
fig = plt.figure(figsize=(16, 12))
gs  = gridspec.GridSpec(3, 3, height_ratios=[1, 1, 1.2], hspace=0.4)

# Pie charts
for idx, (data, title, colors) in enumerate([
    (stage_fear_counts,   "Stage Fear",                [extrovert_color, introvert_color]),
    (drain_counts,        "Drained After Socializing", [extrovert_color, introvert_color]),
    (personality_counts,  "Personality",               color_pair),
]):
    ax = fig.add_subplot(gs[0, idx])
    ax.pie(
        data,
        labels=data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        textprops={"fontsize": 8}
    )
    ax.set_title(title, fontsize=10)

# Helper to plot stacked bars with proper labels
def plot_stacked(ax, df_stacked, xlabel, title):
    df_stacked[ordered_personalities].plot(
        kind="bar", stacked=True,
        color=color_pair, ax=ax
    )
    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel("Number of people", fontsize=9)
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.legend(
        title="Personality",
        labels=ordered_personalities,
        loc="upper right",
        fontsize=8,
        title_fontsize=9
    )

# Middle row
plot_stacked(
    fig.add_subplot(gs[1, 0]),
    stacked_alone,
    "Hours spent alone daily (0–11)",
    "Time Spent Alone"
)
plot_stacked(
    fig.add_subplot(gs[1, 1]),
    stacked_social,
    "Frequency of social events (0–10)",
    "Social Events"
)
plot_stacked(
    fig.add_subplot(gs[1, 2]),
    stacked_outside,
    "Frequency of going outside (0–7)",
    "Going Outside"
)

# Bottom row
plot_stacked(
    fig.add_subplot(gs[2, 0]),
    stacked_friends,
    "Number of close friends (0–15)",
    "Friends Circle"
)
plot_stacked(
    fig.add_subplot(gs[2, 1]),
    stacked_post,
    "Social media post frequency (0–10)",
    "Post Frequency"
)

# Title box
ax = fig.add_subplot(gs[2, 2])
ax.axis("off")
ax.text(
    0.5, 0.5,
    "Extrovert vs. Introvert Behavioral Data Analysis",
    fontsize=12, ha="center", va="center"
)

fig.suptitle("Behavioral Personality Dashboard", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
