import plotly.graph_objects as go
from os import path
from json import load
from random import randint

if not path.exists("prepared_data_default_plot.json"):
    print("Please analyze and prepare data before visualizing it.")
    raise SystemExit

with open("prepared_data_default_plot.json", "r", encoding="utf-8") as f:
    users = load(f)

# Create a blank figure
fig = go.Figure()

# Define colors for the events
colors = [
    f"rgba({randint(0,255)}, {randint(0,255)}, {randint(0,255)}, 0.6598)"
    for _ in range(len(users))
]

showing_names = input(
    "Enter first names of people you want to see or @all to display all (not recommended). Example: name1, name2: "
).split(", ")
print(showing_names)

def extract_first_name(s):
    # Split string by '(' and then ')' to get the username
    firstname = s.split(" ")[0]
    return firstname

yaxis_vals = [] # for alignment 

for i, (name, events) in enumerate(users.items()):
    if (showing_names != ["@all"]) and (extract_first_name(name) not in showing_names):
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

# Set the layout properties

fig.update_layout(
    template="plotly_dark",
    showlegend=True,
    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False,range=[min(yaxis_vals)-15,max(yaxis_vals)+15]),
    xaxis=dict(showgrid=True, zeroline=False, tickformat="%d(th) of %B - %H:%M:%S"),
)

# Show the figure
fig.show()
