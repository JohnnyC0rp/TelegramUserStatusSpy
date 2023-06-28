import plotly.graph_objects as go
from os import path
from json import load
from random import randint

if not path.exists("processed_data\\default_plot.json"):
    print("Please analyze and prepare data before visualizing it.")
    raise SystemExit

with open("processed_data\\default_plot.json", "r", encoding="utf-8") as f:
    users = load(f)

# Create a blank figure
fig = go.Figure()

# Define colors for the events
colors = [
    f"rgba({randint(0,255)}, {randint(0,255)}, {randint(0,255)}, 0.6598)"
    for _ in range(len(users))
]

print(*[f"{i} - {j}\n" for i, j in enumerate(users.keys())])
names = list(users.keys())
showing_names = input("Select people: (Example: 1,2) ")
if showing_names != "@all":
    showing_names = list(map(int, showing_names.split(",")))
else:
    showing_names = list(range(len(names)))

showing_names = [names[i] for i in showing_names]  # here should be names not numbers
print(*showing_names)

yaxis_vals = []  # for alignment

print("Building plot...")

for i, (name, events) in enumerate(users.items()):
    if (showing_names != ["@all"]) and (name not in showing_names):
        continue
    for event in events:
        if len(event) != 2:  # skipping uncompleted events
            continue
        fig.add_trace(
            go.Scatter(
                x=[event[0], event[1]],
                y=[i, i],
                mode="lines+markers",
                line=dict(color=colors[i - 1], width=35),
                marker=dict(size=15),
                hoverinfo="text",
                hovertext=f"{name}<br>Start: {event[0]}<br>End: {event[1]}",
                showlegend=False,
            )
        )
        yaxis_vals.append(i)
    # Add a "dummy" trace for the legend
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color=colors[i - 1], width=35),
            marker=dict(size=10),
            name=name,
            hoverinfo="none",
        )
    )

with open("processed_data\\awake_asleep_times.json", "r", encoding="utf-8") as f:
    awake_asleep = load(f)

if showing_names == "@all":
    print("Warning: sleep time prediction visualization doesn't work with @all.")

else:
    for i in showing_names:
        if i not in awake_asleep:
            print("Cant predict sleep time for", i, "skipping...")
            continue
        fig.add_shape(
            type="line",
            x0=awake_asleep[i][0],
            y0=-1000,
            x1=awake_asleep[i][0],
            y1=1000,
            line=dict(color="green", width=1, dash="dot"),
        )
        fig.add_shape(
            type="line",
            x0=awake_asleep[i][1],
            y0=-1000,
            x1=awake_asleep[i][1],
            y1=1000,
            line=dict(color="cyan", width=1, dash="dot"),
        )

# Set the layout properties

fig.update_layout(
    template="plotly_dark",
    showlegend=True,
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[min(yaxis_vals) - 15, max(yaxis_vals) + 15],
    ),
    xaxis=dict(showgrid=True, zeroline=False, tickformat="%d(th) of %B - %H:%M:%S"),
)
fig.update_layout(title="Online graph", xaxis_title="Time", yaxis_title="Users")

fig.show()
