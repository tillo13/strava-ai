import os
import json

folder = './activities'
files = os.listdir(folder)

# Initialize a dictionary to store suspected Zwift activities file count
zwift_activities = {}

# Loop through each file in the directory
for filename in files:
    # Check if the file is a json file to avoid reading non-json files
    if filename.endswith('.json'):
        # Open the file
        with open(os.path.join(folder, filename), 'r') as file:
            # Load the json content
            data = json.load(file)

            try:
                activity_type = data.get('type')
                external_id = data.get('external_id')
                trainer = data.get('trainer', False)

                # Check if start_latlng and end_latlng exist and are not empty
                start_latlng = data.get('start_latlng', [])
                end_latlng = data.get('end_latlng', [])
                summary_polyline = data.get('map', {}).get('summary_polyline', "")

                # Check if external_id exists, is not None and contains 'zwift-activity' and activity type is 'VirtualRide'
                if external_id is not None and 'zwift-activity' in external_id and activity_type == 'VirtualRide':
                    # Check additional conditions for suspected Zwift activities
                    if not trainer and start_latlng and end_latlng and summary_polyline:
                        # Increment count for suspected Zwift activities
                        zwift_activities[filename] = 1

            except (KeyError, TypeError) as e:
                continue

# Calculate number of other activities
other_activities = len(files) - sum(zwift_activities.values())

# Print number of activities scanned
print(f"We scanned {len(files)} activities.")

# Print number of suspected Zwift activities and other activities
print("We've determined, based on external_id containing 'zwift-activity', activity type='VirtualRide', trainer=false, filled lat/long, and filled summary_polyline, that these are most likely Zwift activities.")
print(f"Zwift activities: {sum(zwift_activities.values())}")
print(f"Other: {other_activities}")