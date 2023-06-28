import plotly.express as px
from os import path
from json import load
from datetime import datetime

if not path.exists("processed_data\\total_time_online.json"):
    print("Please analyze and prepare data before visualizing it.")
    raise SystemExit


def time_to_hours(time_str: str) -> float:
    time_str = time_str.split(".")[0]
    h, m, s = map(int, time_str.split(":"))
    return round(h + (m / 60) + (s / 3600), 3)


with open(
    "processed_data\\total_time_online.json",
    "r",
    encoding="utf-8",
) as f:
    time_online = load(f)

print(*[f"{i} - {j}\n" for i, j in enumerate(time_online.keys())])
names = list(time_online.keys())
choice = input("Select users for comparison or type @all to compare all (ex: 1,2): ")
if choice != "@all":
    choice = map(int, input("Select users for comparison (ex: 1,2): ").split(","))
else:
    choice = list(range(len(names)))

data = {}
for i in choice:
    total_hours = 0
    for time in time_online[names[i]].values():
        total_hours += time_to_hours(time)
    data[total_hours] = names[i]
data = dict(sorted(data.items(), reverse=True))

x = data.values()
y = data.keys()

fig = px.bar(x=x, y=y, template="plotly_dark", color=y)
fig.update_layout(
    title="Users total online time comparison",
    xaxis_title="Users",
    yaxis_title="Total online time (hours)",
)
fig.show()
