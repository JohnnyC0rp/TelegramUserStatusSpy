"""This script prepares data for visualization"""

import json
from os import path, mkdir
import csv
from datetime import datetime
from math import exp

if not path.exists("history.csv"):
    print("Please collect some data before analyzing.")
    exit()

user = {}  # full graph
times_user_got_online = {}
total_time_user_spend_online = {}
awake_asleep_times = {}

delta_time_format = "%H:%M:%S.%f"


def subtract_time(time1: str, time2: str) -> str:
    time1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S.%f")
    time2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S.%f")
    return str(time2 - time1)


def add_time(time1: str, time2: str) -> str:
    dt1 = datetime.strptime(time1, "%H:%M:%S.%f")
    dt2 = datetime.strptime(time2, "%H:%M:%S.%f")

    diff = dt2 - datetime(1900, 1, 1) + (dt1 - datetime(1900, 1, 1))

    return str(diff)


def time_to_seconds(time: str) -> int:
    time = time.split(" ")[1]
    time = time.split(".")[0]
    time = list(map(int, time.split(":")))
    seconds = time[2] + time[1] * 60 + time[0] * 60 * 60
    return seconds


def time_to_seconds(t: str) -> int:
    t = list(map(int, t.split(" ")[1].split(".")[0].split(":")))
    return (t[0] * 60 * 60) + (t[1] * 60) + t[2]


with open("history.csv", "r", encoding="utf-8") as history:
    print(
        "It may take several minutes to process all data, it depends on history.csv size. Please wait."
    )

    reader = csv.reader(history)

    next(reader)  # skip first line
    for row in reader:
        name = f"{row[1] if row[1] else None} {row[2]if row[2] else None} ({row[3]if row[3] else None})"
        status = 1 if row[-1] == "UserStatus.ONLINE" else 0
        time = row[0]
        date = row[0].split(" ")[0]

        if name not in user:
            # first time online
            if status == 1:
                user[name] = [[time]]

                times_user_got_online[name] = {date: 1}

        else:
            # online
            if status and (len(user[name][-1]) == 2):
                user[name].append([time])

                if date in times_user_got_online[name]:
                    times_user_got_online[name][date] += 1
                else:
                    times_user_got_online[name][date] = 1

                if len(user[name]) < 2:
                    continue
                offline_difference = subtract_time(user[name][-2][1], user[name][-1][0])
                if ("day" in offline_difference) or (
                    int(offline_difference.split(":")[0]) > 6
                ):
                    if name in awake_asleep_times:
                        awake_asleep_times[name][0].append(user[name][-1][0])
                        awake_asleep_times[name][1].append(user[name][-2][1])
                    else:
                        awake_asleep_times[name] = [
                            [user[name][-1][0]],
                            [user[name][-2][1]],
                        ]

            # offline
            elif len(user[name][-1]) == 1:
                user[name][-1].append(time)

                if (
                    (
                        (
                            difference := subtract_time(
                                user[name][-1][0], user[name][-1][1]
                            )
                        )
                        == "0:00:00"
                    )
                    or ("day" in difference)
                    or (int(difference.split(":")[0]) > 2)
                ):  # skipping anomalies
                    continue

                if name not in total_time_user_spend_online:
                    total_time_user_spend_online[name] = {date: difference}

                elif date not in total_time_user_spend_online[name]:
                    total_time_user_spend_online[name][date] = difference
                else:
                    total_time_user_spend_online[name][date] = add_time(
                        difference, total_time_user_spend_online[name][date]
                    )


if not path.exists("processed_data"):
    mkdir("processed_data")
    mkdir("processed_data\\clients")

# writing data to json files

# main
with open("processed_data/default_plot.json", "w", encoding="utf-8") as f:
    json.dump(user, f, ensure_ascii=False, indent=4)

# times online
with open("processed_data/time_got_online.json", "w", encoding="utf-8") as f:
    json.dump(times_user_got_online, f, ensure_ascii=False, indent=4)

# total time online
with open("processed_data/total_time_online.json", "w", encoding="utf-8") as f:
    json.dump(total_time_user_spend_online, f, ensure_ascii=False, indent=4)


def get_median_date(date_strings: list) -> str:
    dates = [
        datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
        for date_string in date_strings
    ]
    sorted_dates = sorted(dates)
    length = len(sorted_dates)
    middle_index = length // 2
    median = sorted_dates[middle_index - 1]
    return str(median)


# taking median from awake asleep times
for key, value in awake_asleep_times.items():
    for i, date_list in enumerate(value):
        # Apply your function to each list of dates
        awake_asleep_times[key][i] = get_median_date(date_list)

# times awake asleep
with open("processed_data/awake_asleep_times.json", "w", encoding="utf-8") as f:
    json.dump(awake_asleep_times, f, ensure_ascii=False, indent=4)


print(
    "First part finished, starting second part. It will take much more time than first."
)


def flat_hill(anchors, x, smoothens=5):
    width = smoothens * 100
    slope = smoothens
    delta = abs(anchors[0] - anchors[1])
    if (x >= anchors[0]) and (x <= anchors[1]):
        return 1
    elif (x < (anchors[0] - delta * slope)) or (x > (anchors[1] + delta * slope)):
        return 0
    else:
        return exp(
            -(abs((anchors[0] if x < anchors[0] else anchors[1]) - x) ** 2) / width**2
        )


seconds_in_day = 60 * 60 * 24 + 1  # considering 0
default_smoothens = 10

for key, value in user.items():
    values = [0] * seconds_in_day
    not_smooth_values = [0] * seconds_in_day
    for segment in value:
        if len(segment) < 2:
            continue
        anchors = [time_to_seconds(segment[0]), time_to_seconds(segment[1])]
        for second in range(0, seconds_in_day):
            values[second] += flat_hill(anchors, second, default_smoothens)
            not_smooth_values[second] += flat_hill(anchors, second, 0)

    with open(f"processed_data\\clients\\{key}.json", "w") as f:
        json.dump(values, f)
    with open(f"processed_data\\clients\\{key}_not_smooth.json", "w") as f:
        json.dump(not_smooth_values, f)

    print(f"Data for {key} is ready.")


print("Process finished. Data is ready for visualization.")
