import os
import json

def calculate_score(data):
     #Peloton generally goes of Kilojoules as it is math around cadence/resistance, so you COULD just do: 
    return data['kilojoules']
#however, if you wanted to get my nerdy with it you could: return something like this: 
#    return 1.1 * data['average_speed'] + 1.2 * data['average_watts'] + 1.2 * data['kilojoules']

# Function to determine ride category based on ride duration
def categorize_ride(data):
    duration = data['elapsed_time']/60  # duration in minutes
    categories = [5, 10, 15, 20, 30, 45, 60, 75, 90]
    for category in categories:
        if category - 2 <= duration <= category + 2:
            return category
    return None  # if a ride doesn't fall into any category

# Directory where all the ride data JSON files are stored
directory = './activities'
files = os.listdir(directory)

# Dictionary to hold the ride scores
peloton_ride_scores = {}

# Loop through every file in the directory
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

                # Check if it's a Peloton ride
                if (external_id is not None and external_id.endswith('.tcx') and len(external_id) == 36 and trainer and activity_type == 'Ride' and sport_type == 'Ride'):
                    
                    ride_category = categorize_ride(data)
                    if ride_category is not None:
                        score = calculate_score(data)
                        peloton_ride_scores.setdefault(ride_category, {})[filepath] = score

            except (KeyError, TypeError) as e:
                # Ignore files that cause errors
                continue

categories_order = [90, 75, 60, 45, 30, 20, 15, 10, 5] 

# Sort the peloton_ride_scores dictionary by categories_order
sorted_peloton_ride_scores = {k: peloton_ride_scores[k] for k in categories_order if k in peloton_ride_scores}

# Now, when you loop through sorted_peloton_ride_scores, it will be in the order you specified
for category, rides in sorted_peloton_ride_scores.items():
    sorted_rides = sorted(rides.items(), key=lambda x: x[1], reverse=True)
    print(f'Category: {category} min')
    for ride, score in sorted_rides[:5]:
        print(f'Ride: {ride}, Score: {score}')
    print('---')