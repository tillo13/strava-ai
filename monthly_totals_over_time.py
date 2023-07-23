import os
import json
from collections import defaultdict
from datetime import datetime

folder = './data_cleansing/activities'
files = os.listdir(folder)

# Define subtypes
workout_mapping = {
    'warm up': 'Warm-up',
    'flash 15': 'Core',
    'zen in ten': 'Meditation',
    'fit family': 'Basics',
    'arms & light weights': 'Strength',
    'restorative': 'Meditation',
    'foam rolling': 'Stretch',
    'shadowboxing': 'Core',
    'jumpstart your day': 'Warm-up',
    'mobility': 'Warm-up',
    'flow & let go': 'Warm-up',
    'glutes': 'Lower Body',
    'ride': 'Cycling',
    'bodyweight': 'Strength'
}
workout_subtypes = {'Stretch': 0, 'Strength': 0, 'Meditation': 0, 'Basics': 0, 'Core': 0, 'Pilates': 0, 'Circuit': 0, 'HIIT': 0, 'Cardio': 0, 'Bike Bootcamp': 0, 'Barre': 0, 'Interval': 0, 'Walking': 0, 'Running': 0, 'Tread Bootcamp': 0, 'Yoga': 0, 'Warm-up': 0, 'Bootcamp': 0, 'Arms Toning': 0, 'Full Body': 0, 'Lower Body': 0, 'Upper Body': 0, 'Other': 0}


# Initialize a nested dictionary to store activity counts for each month
activity_counts_by_month = defaultdict(lambda: defaultdict(int))

# Map of source keywords to activity types
activity_source_keywords = {
    'ELEMNT BOLT': 'ELEMNTBOLT',
    'zwift-activity': 'Zwift',
    'garmin_ping': 'GarminPing',
    'activity.fit': 'StravaDirect'
}

activity_display_names = {
    'Ride': 'Peloton Cycling',
    'Run': 'Peloton Run',
    'Walk': 'Peloton Walk',
    'Yoga': 'Peloton Yoga',
    'Workout': 'Peloton Workout',
    'EBikeRide': 'Peloton Ebike Ride',
    'Zwift': 'Zwift Ride',
    'GarminPing': 'Garmin Ping Ride',
    'ELEMNTBOLT': 'ELEMNT BOLT Ride',
    'StravaDirect': 'Strava Direct Ride',
    'Other': 'Unknown'
}

total_activities_by_type = defaultdict(int)
total_months = 0
max_activities = 0
max_month = ""
first_month = None
last_month = None

# Loop through each file in the directory
for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            data = json.load(file)

            try:
                start_date = datetime.strptime(data["start_date"], "%Y-%m-%dT%H:%M:%SZ")
                month_key = start_date.strftime("%Y-%m")  

                if first_month is None or month_key < first_month:
                    first_month = month_key

                if last_month is None or month_key > last_month:
                    last_month = month_key

                activity_type = data.get('type')
                sport_type = data.get('sport_type')
                external_id = data.get('external_id')
                activity_name = data.get('name', '').lower()

                for keyword, source_activity_type in activity_source_keywords.items():
                    if keyword in external_id:
                        activity_type = source_activity_type

                if activity_type == 'Workout' and sport_type == 'Workout':
                    found_mapping = False
                    for specific_workout, category in workout_mapping.items():
                        if specific_workout in activity_name:
                            activity_type = 'Peloton ' + category
                            found_mapping = True 
                            break  
                    if not found_mapping: 
                        # New subtype processing if a workout_mapping match is not found
                        for subtype in workout_subtypes.keys():
                            if subtype.lower() in activity_name:
                                found_mapping = True
                                workout_subtypes[subtype] += 1
                                activity_type = 'Peloton ' + subtype
                                break

                        if not found_mapping:
                            for subtype, mapped_subtype in workout_mapping.items():
                                if subtype in activity_name:
                                    workout_subtypes[mapped_subtype] += 1
                                    activity_type = 'Peloton ' + mapped_subtype
                                    break
                                
                        if not found_mapping:
                            activity_type = 'Peloton Other'

                if activity_type == 'Ride':
                    activity_type = 'Peloton Cycling'

                activity_counts_by_month[month_key][activity_type] += 1
                total_activities_by_type[activity_type] += 1

                if sum(activity_counts_by_month[month_key].values()) > max_activities:
                    max_activities = sum(activity_counts_by_month[month_key].values())
                    max_month = month_key

                total_months = len(activity_counts_by_month.keys())

            except (KeyError, TypeError) as e:
                continue

print(f'We scanned {len(files)} activities from Strava, and found this workout pattern:')

for month in sorted(activity_counts_by_month.keys(), key=lambda x: datetime.strptime(x, "%Y-%m")):
    month_activities = activity_counts_by_month[month]
    print(f"{datetime.strptime(month, '%Y-%m').strftime('%Y-%B')}: ", end="")
    print(", ".join(f"{count} {activity_display_names.get(activity_type, activity_type)} activities"
                    for activity_type, count in month_activities.items()))   

print('=============')
print(f'We tracked {total_months} months, from {datetime.strptime(first_month, "%Y-%m").strftime("%Y-%B")} to {datetime.strptime(last_month, "%Y-%m").strftime("%Y-%B")} and found...')    

print(f'\nYour MOST active month was {max_month} with {max_activities} total activities across all platforms.')

print('\nYour AVERAGE month has:')
sorted_activities = sorted(total_activities_by_type.items(), key=lambda item: (item[0].startswith("Peloton"), item[1]), reverse=True)
for activity_type, total in sorted_activities:
    print(' {:.2f} {} activities'.format(total/total_months, activity_display_names.get(activity_type, activity_type)))