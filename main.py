"""This script collects data"""

from pyrogram import Client
from pyrogram.handlers import UserStatusHandler
import os
from datetime import datetime
import csv

try:
    from api_info import *
except ModuleNotFoundError:
    print("Please create file 'api_info.py' and put there your api_id and api_hash.")
    exit()

if not os.path.exists("pyrogram_session"):
    os.makedirs("pyrogram_session")

names = {}  # id:(name,lastname,username)

if not os.path.exists("history.csv"):
    history = open("history.csv", "a+", encoding="utf-8", newline="")
    writer = csv.writer(history)
    writer.writerow(
        ["Time", "Timestamp", "First name", "Last name", "Username", "Status"]
    )
else:
    history = open("history.csv", "a+", encoding="utf-8", newline="")
    writer = csv.writer(history)


def handle_status_change(client, user):
    if user.id in names:
        info = f"{datetime.now()}: {names[user.id][0]} {names[user.id][1]} ({names[user.id][2]}) is {user.status}"
        print(info)

    else:
        user_details = client.get_users(user.id)
        names[user.id] = (
            user_details.first_name,
            user_details.last_name,
            user_details.username,
        )
        info = f"{datetime.now()}: {user_details.first_name} {user_details.last_name} ({user_details.username}) is {user.status} - [NEW USER, DATA SAVED]"
        print(info)

    writer.writerow(
        [
            current_time := datetime.now(),
            datetime.timestamp(current_time),
            names[user.id][0],
            names[user.id][1],
            names[user.id][2],
            user.status,
        ]
    )
    history.flush()


# ----------- Initializing clients ----------------


app = Client(
    "spy_session",
    workdir="pyrogram_session/",
    api_hash=api_hash,
    api_id=api_id,
)
app.add_handler(UserStatusHandler(handle_status_change))


app.run()
