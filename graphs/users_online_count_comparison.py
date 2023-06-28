import plotly.express as px
from os import path
from json import load

if not path.exists("processed_data\\time_got_online.json"):
    print("Please analyze and prepare data before visualizing it.")
    raise SystemExit


def count_sum(d: dict) -> int:
    return sum(list(d.values()))


with open(
    "processed_data\\time_got_online.json",
    "r",
    encoding="utf-8",
) as f:
    users = load(f)

print(*[f"{i} - {j}\n" for i, j in enumerate(users.keys())])
showing_names = input(
    "Select people for comparison or @all to display all: (Example: 1,2)"
)
if showing_names != "@all":
    showing_names = list(
        map(
            int,
            showing_names.split(","),
        )
    )
names = list(users.keys())
if showing_names != "@all":
    showing_names = [
        names[i] for i in showing_names
    ]  # here should be names not numbers
else:
    showing_names = names
data = {count_sum(users[i]): i for i in showing_names}
data = dict(sorted(data.items(), reverse=True))
x = list(data.values())
y = list(data.keys())

fig = px.bar(x=x, y=y, color=y, template="plotly_dark")
fig.update_layout(
    title="Total online time comparison",
    xaxis_title="Users",
    yaxis_title="Total time online",
)
fig.show()
