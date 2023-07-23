import os
import json

folder = './activities'
files = os.listdir(folder)

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
# Loop through each file in the directory
for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            data = json.load(file)

            activity_type = data.get('type')
            sport_type = data.get('sport_type')

            # Process workouts and look for the unknown subtypes
            if activity_type == 'Workout' and sport_type == 'Workout':
                name = data.get('name', '').lower()
                found_subtype = False
                for subtype in workout_subtypes.keys():
                    if subtype.lower() in name:
                        found_subtype = True
                        workout_subtypes[subtype] += 1
                        break  # found a match, no need to continue loop
                
                # Check if not found in standard subtypes
                if not found_subtype:
                    for subtype, mapped_subtype in workout_mapping.items():
                        if subtype in name:
                            found_subtype = True
                            workout_subtypes[mapped_subtype] += 1
                            break  # found a match, no need to continue loop
                
                if not found_subtype:
                    print(name)