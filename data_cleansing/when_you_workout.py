import os
import json
import statistics
from datetime import datetime
from collections import defaultdict
from pytz import timezone
from tabulate import tabulate
from termcolor import colored

# define timezone string
time_zone = 'America/Los_Angeles'

folder = './data_cleansing/activities'
files = os.listdir(folder)

#this remove the top and bottom % of values before calculating the averages in case of outliers
TRIM_VALUE = .005
def remove_outliers(values):
    values.sort()
    outliers_removed = values[int(len(values)*TRIM_VALUE):-int(len(values)*TRIM_VALUE)]
    return outliers_removed if outliers_removed else values

def color_rows(rows, attrs):
    max_values = {attr: max(row[i] for row in rows if row[i] != 'N/A') for i, attr in enumerate(attrs, 2)}
    min_values = {attr: min(row[i] for row in rows if row[i] != 'N/A') for i, attr in enumerate(attrs, 2)}
    colored_rows = []
    for row in rows:
        colored_row = []
        for i, value in enumerate(row):
            if i < 2 or value == 'N/A':
                colored_row.append(value)
            else:
                attr = attrs[i - 2]
                if value == max_values[attr]:
                    colored_row.append(colored(value, 'green'))
                elif value == min_values[attr]:
                    colored_row.append(colored(value, 'blue'))
                else:
                    colored_row.append(value)
        colored_rows.append(colored_row)
    return colored_rows

# Define our timezone as variable time_zone (Seattle's timezone for this case)
custom_tz = timezone(time_zone)

# Initialize a dictionary to store workout counts for each hour of the day
workouts_per_hour = defaultdict(int)

# Attributes to store average
attrs = ['max_heartrate', 'average_heartrate', 'kilojoules', 'weighted_average_watts', 'max_watts', 'average_watts', 'average_cadence', 'max_speed', 'average_speed', 'elapsed_time', 'distance']

# Initialize a dictionary to store the values of these attributes for each hour
attr_values = defaultdict(lambda: defaultdict(list))

for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            data = json.load(file)

            try:
                start_date_local = data.get('start_date_local')
                if start_date_local:
                    start_datetime = datetime.strptime(start_date_local, "%Y-%m-%dT%H:%M:%SZ")
                    custom_time = start_datetime.astimezone(custom_tz)
                    workouts_per_hour[custom_time.hour] += 1

                    for attr in attrs:
                        value = data.get(attr)
                        if value is not None:
                            if attr == 'elapsed_time':
                                value /= 60
                            elif attr == 'distance':
                                value /= 1609.34
                            attr_values[custom_time.hour][attr].append(value)

            except (ValueError, KeyError, TypeError) as e:
                continue

table_data = []

print(f"Hour of Day ({time_zone}) - Number of Workouts - Average Values")
for hour in range(24):  
    if hour in workouts_per_hour:
        count = workouts_per_hour[hour]
        averages = {attr: round(statistics.mean(remove_outliers(attr_values[hour][attr])), 2) for attr in attrs if attr_values[hour][attr]}
        row = [hour, count] + [averages.get(attr, 'N/A') for attr in attrs]
    else:
        row = [hour, 0] + ['N/A' for _ in attrs]
    table_data.append(row)

table_data = color_rows(table_data, attrs)
print(tabulate(table_data, headers=['Hour', 'Workouts'] + attrs))