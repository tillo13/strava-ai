import requests
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Define URL and your client's details
url = 'https://www.strava.com/oauth/token'
payload = {
    'client_id': os.getenv('STRAVA_CLIENT_ID'),
    'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
    'code': '<anything here for now>',  # replace with your authorization code
    'grant_type': 'authorization_code'
}

response = requests.post(url, data=payload)

# Print the response
print(response.text)

# Parse the JSON response
json_response = response.json()

# Save the tokens to your CSV file
with open('access_tokens.csv', mode='a') as file:
    fieldnames = ['client_id', 'access_token', 'expires_at', 'refresh_token']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writerow({
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'access_token': json_response.get('access_token'),
        'expires_at': json_response.get('expires_at'),
        'refresh_token': json_response.get('refresh_token'),
    })