import plotly.express as px
from os import path
from json import load

if not path.exists("processed_data/time_got_online.json"):
    print("Please analyze and prepare data before visualizing it.")
    raise SystemExit


with open(
    "processed_data/time_got_online.json",
    "r",
    encoding="utf-8",
) as f:
    users = load(f)

print(*[f"{i} - {j}\n" for i, j in enumerate(users.keys())])
first_name = int(input("Select person: "))
data = list(users.values())[first_name]
x = data.keys()
y = data.values()

fig = px.bar(x=x, y=y, color=y, template="plotly_dark")
fig.update_layout(
    title=f"Online count comparison by days for {list(users.keys())[first_name]}",
    xaxis_title="Days",
    yaxis_title="Online count",
    xaxis=dict(dtick="1D"),
)

fig.show()
