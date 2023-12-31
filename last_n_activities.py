import os
import requests
from initialize import check_token
import json
import time
import sys

# Proceed with the API call
access_token = check_token()  # This will give you the latest access token

url = "https://www.strava.com/api/v3/athlete/activities"

headers = {
    'Authorization': f'Bearer {access_token}'
}

params = {
    'per_page': 7,  # Number of activities per page
    'page': 1  # Page number
}

response = requests.get(url, headers=headers, params=params)

# check if the response is JSON
try:
    activities = response.json()
except json.JSONDecodeError:
    print(f"Error decoding JSON response: {response.text}")
    sys.exit(1)

# ensure the activities object is a list
if not isinstance(activities, list):
    print(f"Unexpected API response: {activities}")
    sys.exit(1)

# continue with your original code...
folder_path = './activities'
os.makedirs(folder_path, exist_ok=True)

# Get a list of existing files in the 'activities' folder
existing_files = os.listdir(folder_path)

# Save each activity as a separate file, checking for duplicates
activities = response.json()
num_duplicates = 0
num_new_activities = 0
start_time = time.time()

for activity in activities:
    activity_id = activity['id']
    file_path = os.path.join(folder_path, f'{activity_id}.json')
    
    if f'{activity_id}.json' in existing_files:
        num_duplicates += 1
        continue
    
    with open(file_path, 'w') as file:
        json.dump(activity, file, indent=4)
    num_new_activities += 1

# Introduce a delay to accurately measure the script run time
time.sleep(1)

end_time = time.time()
script_run_time = end_time - start_time

# Print the requested terminal output
requested_activities = params['per_page']
print(f"Requested activities: {requested_activities}")
print(f"Duplicates: {num_duplicates} files already exist in the 'activities' folder.")
print(f"New activities: {num_new_activities} new files were created.")
print(f"Script run time: {script_run_time} seconds.")
