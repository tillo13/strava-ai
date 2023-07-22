import os, json
import pandas as pd

activities_folder = 'activities'  # Update the path to match your folder structure
json_files = [file for file in os.listdir(activities_folder) if file.endswith('.json')]

rides = []

for file_name in json_files:
    with open(os.path.join(activities_folder, file_name), 'r') as file:
        data = json.load(file)
        activity_type = data.get('type')
        if activity_type == 'Ride':  # We're only interested in "Ride" activities
            ride_id = data.get('id')
            average_watts = data.get('average_watts')
            distance = data.get('distance') / 1609.344  # Converting meters to miles
            kilojoules = data.get('kilojoules')
            score = average_watts * distance * kilojoules if all([average_watts, distance, kilojoules]) else None
            rides.append({'ride_id': ride_id, 'average_watts': average_watts, 'distance': distance, 'kilojoules': kilojoules, 'score': score})

# Now we create a dataframe and print the top 5 rides for each length of ride desired
df = pd.DataFrame(rides)

def round_minutes(minutes):
    # Use this function to round times to nearest 5 minutes
    return round(minutes / 5) * 5

df['RideTime'] = df['distance'].apply(round_minutes)

# Get top 5 rides by any metric for each RideTime
top_rides = df.groupby('RideTime').apply(lambda x: x.nlargest(5, 'score'))

print(top_rides[['ride_id', 'average_watts', 'distance', 'kilojoules', 'score']])