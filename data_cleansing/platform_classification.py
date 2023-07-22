import json
import os
import re

# Initialization
workout_count = {'Zwift Rides': 0, 'Peloton Yoga': 0, 'Peloton Cycling Rides': 0, 'Strength workouts': 0, 'Others': 0}

# Traverse the directory with data files
for filename in os.listdir('./activities'): 
    with open(os.path.join('./activities', filename), 'r') as f:
        workout = json.load(f)

    # Identify Zwift workout
    if workout['type'] == 'VirtualRide' and 'zwift' in workout['name'].lower() and 'summary_polyline' in workout['map']:
        workout_count['Zwift Rides'] += 1
    
    # Identify Peloton Yoga workouts
    elif workout['external_id'] is not None and 'tcx' in workout['external_id'] and workout['distance']==0.0 and 'yoga' in workout['name'].lower():
        workout_count['Peloton Yoga'] += 1

    # Identify Peloton Cycling rides
    elif 'ride with' in workout['name'].lower() and len(workout['start_latlng'])==0:
        workout_count['Peloton Cycling Rides'] += 1

    # For strength workouts etc.
    # elif condition:
        # workout_count['Strength workouts'] += 1
    
    # For others
    else:
        workout_count['Others'] += 1

# Display result
total = sum(workout_count.values())
for workout, count in workout_count.items():
    percentage = (count / total) * 100
    print(f"{count} ({percentage:.3f}%) {workout}")