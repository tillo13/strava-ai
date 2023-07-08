import os
import requests
from initialize import check_token

# Check and update the token 
check_token()

# Get the user ID from user input
user_id = input("Enter the Strava user ID: ")

# Retrieve athlete data from user ID
athlete_url = f"https://www.strava.com/api/v3/athletes/{user_id}"
access_token = os.getenv('STRAVA_ACCESS_TOKEN')
headers = {
    'Authorization': f'Bearer {access_token}'
}
athlete_response = requests.get(athlete_url, headers=headers)
athlete_data = athlete_response.json()

# Print the JSON results
print("JSON Results:")
print(athlete_data)
