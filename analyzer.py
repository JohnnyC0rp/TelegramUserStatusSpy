"""This script prepares data for visualization"""

import json
from os import path
import csv

if not path.exists("history.csv"):
    print("Please collect some data before analyzing.")
    exit()

users = {}

with open("history.csv", "r", encoding="utf-8") as history:
    reader = csv.reader(history)

    next(reader)  # skip first line
    for row in reader:
        name = f"{row[1] if row[1] else None} {row[2]if row[2] else None} ({row[3]if row[3] else None})"
        status = 1 if row[-1] == "UserStatus.ONLINE" else 0
        time = row[0]

        if name not in users:
            if status == 1:
                users[name] = [[time]]

        else:
            if status and (len(users[name][-1]) == 2):
                users[name].append([time])
            elif len(users[name][-1]) == 1:
                users[name][-1].append(time)


with open("prepared_data_default_plot.json", "w", encoding="utf-8") as f:
    json.dump(users, f, ensure_ascii=False, indent=4)
