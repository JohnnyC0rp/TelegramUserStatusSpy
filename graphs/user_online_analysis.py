import plotly.express as px
from os import path, listdir
from json import load
from datetime import datetime, timedelta

if not path.exists("processed_data\\clients"):
    print("Please analyze and prepare data before visualizing it.")
    raise SystemExit


def generate_x_axes_values():
    global x
    start_time = datetime.strptime("00:00:00", "%H:%M:%S")
    delta = timedelta(seconds=1)
    x = [
        "2000-01-01 " + str((start_time + i * delta).time())
        for i in range(60 * 60 * 24)
    ] + ["2000-01-01 24:00:00"]


for i, name in enumerate(listdir("processed_data\\clients")):
    if "_not_smooth" not in name:
        print(f"{i//2} - {name.replace('.json','')}")
choice = listdir("processed_data\\clients")[(int(input("Select user: ")) * 2)].replace(
    ".json", ""
)

with open(
    f"processed_data\\clients\\{choice}.json",
    "r",
    encoding="utf-8",
) as f:
    online_intensity_smooth = load(f)
with open(
    f"processed_data\\clients\\{choice}_not_smooth.json",
    "r",
    encoding="utf-8",
) as f:
    print(f"processed_data\\clients\\{choice}_not_smooth.json")
    online_intensity = load(f)

generate_x_axes_values()
y = online_intensity
y_smooth = online_intensity_smooth

fig = px.area(x=x, y=y_smooth)
fig.add_scatter(x=x, y=y, mode="lines", name="Raw")
fig.update_layout(xaxis=dict(nticks=24, tickformat="%H:%M"), template="plotly_dark")
fig.update_layout(
    title=f"{choice}'s online intensity", xaxis_title="24H Time", yaxis_title="Online Count"
)
fig.show()
