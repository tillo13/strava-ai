import os
import json
from collections import defaultdict

folder = './activities'
files = os.listdir(folder)

peloton_types = defaultdict(int)
peloton_sport_types = defaultdict(int)

# Loop through each file in the directory
for filename in files:
    # Check to make sure the file is a json file to avoid reading non-json files
    if filename.endswith('.json'):
        # Open the file
        with open(os.path.join(folder, filename), 'r') as file:
            # Load the json content
            data = json.load(file)

            try:
                external_id = data.get('external_id')
                trainer = data.get('trainer', False)
                start_latlng = data.get('start_latlng', [])
                end_latlng = data.get('end_latlng', [])
                activity_type = data.get('type')
                sport_type = data.get('sport_type')

                # Check conditions for suspected Peloton activities
                if external_id is not None and external_id.endswith('.tcx') and len(external_id) == 36:
                    if trainer and not start_latlng and not end_latlng:
                        # Count the unique types and sport types for Peloton activities
                        if activity_type is not None:
                            peloton_types[activity_type] += 1
                        if sport_type is not None:
                            peloton_sport_types[sport_type] += 1
                
            except (KeyError, TypeError) as e:
                continue

print(f"We scanned {len(files)} activities.")

print("Unique 'type' values and their counts in Peloton activities:")
for k, v in peloton_types.items():
    print(f"Type: {k}, Count: {v}")

print("\nUnique 'sport_type' values and their counts in Peloton activities:")
for k, v in peloton_sport_types.items():
    print(f"Sport Type: {k}, Count: {v}")