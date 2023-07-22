import os
import json

activities_folder = 'activities'  # Update the path to match your folder structure
json_files = [file for file in os.listdir(activities_folder) if file.endswith('.json')]

# Info for your specific Peloton ride
specific_distance_miles = 17.93
specific_avg_watts = 279

# converting distance from miles to meters
specific_distance_meters = specific_distance_miles * 1609.34

for file_name in json_files:
    with open(os.path.join(activities_folder, file_name), 'r') as file:
        data = json.load(file)

        # Extracting distance and average watts from the Strava JSON data
        strava_distance = data.get('distance')
        strava_avg_watts = data.get('average_watts')

        # Extracting external_id and activity type
        external_id = data.get('external_id')
        activity_type = data.get('type')

        # Check  external_id and activity type specifically for Peloton ride.
        if external_id is not None and external_id.endswith('.tcx') and len(external_id) == 36:
            if activity_type == "Ride":
                # introduce a threshold to match the values approximately
                distance_tolerance = 1000  # meters
                watts_tolerance = 5  # watts

                # Comparing the Strava JSON data with the specific Peloton ride info
                if (abs(specific_distance_meters - strava_distance) <= distance_tolerance) and \
                    (abs(specific_avg_watts - strava_avg_watts) <= watts_tolerance):
                    print(f"Found the peloton ride! The file name is: {file_name}")
                    print(json.dumps(data, indent=4))  # Pretty print the JSON data
                    break
else:
    print("Could not find the ride.")
