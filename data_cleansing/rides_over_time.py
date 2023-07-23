import os
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

directory = './data_cleansing/activities'
files = os.listdir(directory)

# Step 1: Extract the metrics and ride dates
dates = []
average_speeds = []
distances = []
kj_values = []

for filename in files:
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r') as file:
            data = json.load(file)

            try:
                external_id = data.get('external_id')
                trainer = data.get('trainer', False)
                activity_type = data.get('type')
                sport_type = data.get('sport_type')

                if (external_id is not None and external_id.endswith('.tcx') and len(external_id) == 36 and trainer and activity_type == 'Ride' and sport_type == 'Ride'):
                    ride_time = datetime.strptime(data['start_date_local'], '%Y-%m-%dT%H:%M:%SZ')  # convert to datetime
                    average_speed = data.get('average_speed') * 2.237 if data.get('average_speed') else None  # km/h to miles/h
                    total_distance = data.get('distance', 'N/A') / 1609 if data.get('distance') else None # meter to mile
                    kilojoules = data.get('kilojoules', 'N/A')

                    if average_speed is not None and total_distance is not None and kilojoules is not None:
                        dates.append(ride_time)
                        average_speeds.append(average_speed)
                        distances.append(total_distance)
                        kj_values.append(kilojoules)

            except (KeyError, TypeError):
                continue

# create a Dataframe
df = pd.DataFrame({'avg_speed': average_speeds, 'distance': distances, 'kilojoules': kj_values}, index=dates)
df.sort_index(inplace=True)  # sort by date

# Step 2-4: Aggregate the metrics per time period and plot
for column in df.columns:
    df_monthly = df[column].resample('M').mean()
    plt.figure(figsize=(10, 6))
    plt.plot(df_monthly.index, df_monthly.values, '-o')
    plt.xlabel('Month')
    plt.ylabel(column)
    plt.title(f'Monthly Average {column}')
    plt.show()