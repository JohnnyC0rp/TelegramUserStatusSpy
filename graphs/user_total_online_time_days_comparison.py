import plotly.express as px
from os import path
from json import load

if not path.exists("processed_data\\total_time_online.json"):
    print("Please analyze and prepare data before visualizing it.")
    raise SystemExit


with open(
    "processed_data\\total_time_online.json",
    "r",
    encoding="utf-8",
) as f:
    users = load(f)

print(*[f"{i} - {j}\n" for i, j in enumerate(users.keys())])
choice = int(input("Select user: "))
names = list(users.keys())
data = users[names[choice]]
x = list(data.keys())
y = ["2000-01-01 " + i for i in data.values()]
fig = px.bar(x=x, y=y, template="plotly_dark")

fig.update_xaxes(tickformat="%d-%b", dtick="D1")  # Example format: '01-Jun'
fig.update_yaxes(tickformat="%H:%M:%S")
fig.update_layout(
    title=f"Total time online days comparison for {names[choice]}",
    xaxis_title="Days",
    yaxis_title="Time online",
)
fig.show()
