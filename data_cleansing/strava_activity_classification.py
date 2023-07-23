import os
import json

folder = './activities'
files = os.listdir(folder)

# Initialize a dictionary to store filed counts for each type of activity
peloton_activities = {'Ride': 0, 'Yoga': 0, 'EBikeRide': 0, 'Run': 0, 'Walk': 0, 'Workout': 0, 'Other': 0}
workout_subtypes = {'Stretch': 0, 'Strength': 0, 'Meditation': 0, 'Basics': 0, 'Core': 0, 'Pilates': 0, 'Circuit': 0, 'HIIT': 0, 'Cardio': 0, 'Bike Bootcamp': 0, 'Barre': 0, 'Interval': 0, 'Walking': 0, 'Running': 0, 'Tread Bootcamp': 0, 'Yoga': 0, 'Warm-up': 0, 'Bootcamp': 0, 'Arms Toning': 0, 'Full Body': 0, 'Lower Body': 0, 'Upper Body': 0, 'Other': 0}

# Map of specific workouts to workout categories
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
    'ride' : 'Basics',
    'bodyweight' : 'Strength'
}


elemnt_bolt_activities = {}
zwift_activities = {}
garmin_ping_activities = {}
strava_direct_activities = {}
other_activities_count = 0

# Loop through each file in the directory
for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            data = json.load(file)

            try:
                external_id = data.get('external_id')
                trainer = data.get('trainer', False)
                activity_type = data.get('type')
                sport_type = data.get('sport_type')
                start_latlng = data.get('start_latlng', [])
                end_latlng = data.get('end_latlng', [])
                summary_polyline = data.get('map', {}).get('summary_polyline', "")

                # U
                # Update workout subtypes if the activity is a "Workout"
                if activity_type == 'Workout' and sport_type == 'Workout':
                    name = data.get('name', '').lower()
                    found_mapping = False
                    for specific_workout, category in workout_mapping.items():
                        if specific_workout in name:
                            workout_subtypes[category] += 1
                            found_mapping = True
                            break  # found a match, no need to continue loop
                    if not found_mapping:  # if no specific workout match, fallback to older logic
                        found_subtype = False
                        for subtype in workout_subtypes.keys():
                            if subtype.lower() in name:
                                workout_subtypes[subtype] += 1
                                found_subtype = True
                                break  # found a match, no need to continue loop
                        if not found_subtype:
                            workout_subtypes['Other'] += 1

                if external_id is not None and external_id.endswith('.tcx') and len(external_id) == 36:
                    if trainer and not start_latlng and not end_latlng:
                        if activity_type in peloton_activities.keys() and sport_type == activity_type:
                            peloton_activities[activity_type] += 1
                        else:  # for unknown activity types
                            peloton_activities['Other'] += 1
                        continue

                if 'ELEMNT BOLT' in external_id and not trainer and start_latlng and end_latlng and summary_polyline:
                    elemnt_bolt_activities[filename] = 1
                    continue

                if 'zwift-activity' in external_id and activity_type == 'VirtualRide':
                    if not trainer and start_latlng and end_latlng and summary_polyline:
                        zwift_activities[filename] = 1
                        continue

                if 'garmin_ping' in external_id and not trainer and start_latlng and end_latlng and summary_polyline:
                    garmin_ping_activities[filename] = 1
                    continue

                if 'activity.fit' in external_id and len(external_id) == 49:
                    if not trainer and start_latlng and end_latlng and summary_polyline:
                        strava_direct_activities[filename] = 1
                        continue

                other_activities_count += 1

            except (KeyError, TypeError) as e:
                continue

print(f'We scanned {len(files)} activities from Strava and sorted by various JSON values.  Specifically to Peloton, type/sport_type JSON values merged with external_ID')
peloton_activities_sorted = sorted(peloton_activities.items(), key=lambda x: x[1], reverse=True)

for activity, count in peloton_activities_sorted:
    if activity == "Workout":
        print(f"   -> {count} of them were of sport_type=Workout, which includes:")
        workout_subtypes_sorted = sorted(workout_subtypes.items(), key=lambda x: x[1], reverse=True)
        for subtype, subtype_count in workout_subtypes_sorted:
            if subtype_count > 0:
                print(f"    ->> {subtype_count} {subtype if subtype != 'Other' else 'Unknown'} workouts")
    else:
         print(f"   -> {count} of them were Peloton sport_type = {activity if activity != 'Other' else 'Unknown'}.")

print(f"===Non-Peloton activities===")
print(f"ELEMNT BOLT activities: {len(elemnt_bolt_activities)}")
print(f"Zwift activities: {len(zwift_activities)}")
print(f"Garmin Ping activities: {len(garmin_ping_activities)}")
print(f"Strava direct activities: {len(strava_direct_activities)}")
print(f"Unknown platform activities: {other_activities_count}")