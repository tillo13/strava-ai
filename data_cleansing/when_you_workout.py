import os
import json
from datetime import datetime
from collections import defaultdict
from pytz import timezone

# define timezone string
time_zone = 'America/Los_Angeles'

folder = './data_cleansing/activities'
files = os.listdir(folder)

# Define our timezone as variable time_zone (Seattle's timezone for this case)
custom_tz = timezone(time_zone)

# Initialize a dictionary to store workout counts for each hour of the day
workouts_per_hour = defaultdict(int)

# Loop through each file in the directory
for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            data = json.load(file)

            try:
                # Get start date in local time
                start_date_local = data.get('start_date_local')
                if start_date_local:
                    # Convert string into datetime object
                    start_datetime = datetime.strptime(start_date_local, "%Y-%m-%dT%H:%M:%SZ")
                    # Convert it to custom timezone
                    custom_time = start_datetime.astimezone(custom_tz)
                    # Increase the workout count of the corresponding hour
                    workouts_per_hour[custom_time.hour] += 1

            except (ValueError, KeyError, TypeError) as e:
                continue

# Sort workouts per hour by hour
workouts_per_hour_sorted = sorted(workouts_per_hour.items())

print(f"Hour of Day ({time_zone}) - Number of Workouts")
for hour, count in workouts_per_hour_sorted:
    print(f"{hour:02d}:00 - {count}")