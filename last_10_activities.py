from dotenv import load_dotenv
import os
import requests
from initialize import check_token
import json

load_dotenv()

# Check and update the token 
check_token()

# Proceed with the API call
access_token = os.getenv('STRAVA_ACCESS_TOKEN')

url = "https://www.strava.com/api/v3/athlete/activities"

headers = {
    'Authorization': f'Bearer {access_token}'
}

params = {
    'per_page': 3,  # Number of activities per page
    'page': 1  # Page number
}

response = requests.get(url, headers=headers, params=params)

# Format and print the JSON response
formatted_response = json.dumps(response.json(), indent=4)
print(formatted_response)
