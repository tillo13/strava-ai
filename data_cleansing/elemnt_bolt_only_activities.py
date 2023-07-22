import os
import json

folder = './activities'
files = os.listdir(folder)

# Initialize a dictionary to store file count for suspected ELEMNT BOLT activities
elemnt_bolt_activities = {}

# Loop through each file in the directory
for filename in files:
    # Check if the file is a json file to avoid reading non-json files
    if filename.endswith('.json'):
        # Open the file
        with open(os.path.join(folder, filename), 'r') as file:
            # Load the json content
            data = json.load(file)

            try:
                external_id = data.get('external_id')
                trainer = data.get('trainer', False)

                # Check if start_latlng and end_latlng exist and are not empty
                start_latlng = data.get('start_latlng', [])
                end_latlng = data.get('end_latlng', [])
                summary_polyline = data.get('map', {}).get('summary_polyline', "")

                # Check if external_id exists, is not None and includes 'ELEMNT BOLT'
                if external_id is not None and 'ELEMNT BOLT' in external_id:
                    # Check additional conditions for suspected ELEMNT BOLT activities
                    if not trainer and start_latlng and end_latlng and summary_polyline:
                        # Increment count for suspected ELEMNT BOLT activities
                        elemnt_bolt_activities[filename] = 1

            except (KeyError, TypeError) as e:
                continue

# Calculate number of other activities
other_activities = len(files) - sum(elemnt_bolt_activities.values())

# Print number of activities scanned
print(f"We scanned {len(files)} activities.")

# Print number of suspected ELEMNT BOLT activities and other activities
print("We've determined, based on external_id including 'ELEMNT BOLT', trainer=false, filled lat/long, and filled summary_polyline that these are most likely ELEMNT BOLT activities.")
print(f"ELEMNT BOLT activities: {sum(elemnt_bolt_activities.values())}")
print(f"Other: {other_activities}")