import pandas as pd
import json
import os

folder = './activities'  
files = os.listdir(folder)
data_list = []

for file in files:
    with open(os.path.join(folder, file), 'r') as f:
        workout = json.load(f)
        
        temp_dict = {}
        temp_dict['type'] = workout.get('type', None)
        temp_dict['distance'] = workout.get('distance', None)
        temp_dict['moving_time'] = workout.get('moving_time', None)
        temp_dict['total_elevation_gain'] = workout.get('total_elevation_gain', None)
        temp_dict['average_speed'] = workout.get('average_speed', None)
        temp_dict['max_speed'] = workout.get('max_speed', None)
        temp_dict['average_cadence'] = workout.get('average_cadence', None)
        temp_dict['average_watts'] = workout.get('average_watts', None)
        temp_dict['max_watts'] = workout.get('max_watts', None)
        
        # Extract year, month, day, hour from start_date_local
        if 'start_date_local' in workout:
            start_date = pd.to_datetime(workout['start_date_local'])
            temp_dict['year'] = start_date.year
            temp_dict['month'] = start_date.month
            temp_dict['day'] = start_date.day
            temp_dict['hour'] = start_date.hour
            
        data_list.append(temp_dict)

df = pd.DataFrame(data_list)

# Print the DataFrame
print(df.head())