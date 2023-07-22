import os
import json

folder = './activities'
files = os.listdir(folder)

# Initialize a dictionary to store file types and their count for suspected Peloton activities
peloton_activities = {}

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

                # Check if start_latlng and end_latlng exist and are empty
                start_latlng = data.get('start_latlng', [])
                end_latlng = data.get('end_latlng', [])

                # Check if external_id exists and is not None
                if external_id is not None:
                    file_extension = os.path.splitext(external_id)[1]

                    # Check if the extension is '.tcx' and the external_id is 36 characters long
                    if file_extension == '.tcx' and len(external_id) == 36:
                        # Check additional conditions for suspected Peloton activities
                        if trainer and not start_latlng and not end_latlng:
                            # Increment count for suspected Peloton activities
                            peloton_activities[file_extension] = peloton_activities.get(file_extension, 0) + 1

            except (KeyError, TypeError) as e:
                continue
                
# Calculate number of other activities
other_activities = len(files) - sum(peloton_activities.values())

# Print number of activities scanned
print(f"We scanned {len(files)} activities.")

# Print number of suspected Peloton activities and other activities
print("We've determined, based on external_id=36 alphanumeric characters with a .tcx extension, trainer=true, and lat/long=null that these are most likely Peloton activities.")
print(f"Peloton activities: {sum(peloton_activities.values())}")
print(f"Other: {other_activities}")