#2023july7 Rate Limits = 200 requests every 15 minutes, 2,000 daily
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
from pytz import timezone

load_dotenv()

def get_new_token():
    url = "https://www.strava.com/oauth/token"

    payload = {
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
        'grant_type': 'refresh_token',
        'f': 'json'
    }

    response = requests.post(url, params=payload)
    response_json = response.json()

    # Write the new values to the .env file
    with open('.env', 'w') as file:
        file.write(f"STRAVA_CLIENT_ID={os.getenv('STRAVA_CLIENT_ID')}\n")
        file.write(f"STRAVA_CLIENT_SECRET={os.getenv('STRAVA_CLIENT_SECRET')}\n")
        file.write(f"STRAVA_REFRESH_TOKEN={response_json['refresh_token']}\n")
        file.write(f"STRAVA_ACCESS_TOKEN={response_json['access_token']}\n")
        file.write(f"STRAVA_TOKEN_EXPIRES_AT={response_json['expires_at']}\n")
        # Update STRAVA_LAST_CHECKED
        file.write(f"STRAVA_LAST_CHECKED={datetime.now().timestamp()}") 

    expires_at_seattle = datetime.fromtimestamp(response_json['expires_at'], tz=timezone('US/Pacific'))
    print(f"New token expires_at: {expires_at_seattle}")

def check_token():
    # Load the expiry time from .env and default to current timestamp
    expires_at = float(os.getenv('STRAVA_TOKEN_EXPIRES_AT', datetime.now().timestamp()))

    # Get the current timestamp
    now = round(datetime.now().timestamp())

    strava_last_checked = datetime.now().timestamp()  # Store the current timestamp for the last checked time
    strava_last_checked_seattle = datetime.fromtimestamp(strava_last_checked, tz=timezone('US/Pacific'))  # Convert to Seattle timezone
    
    # If the token has expired
    if now > expires_at:
        get_new_token()
    else:
        time_left = abs(expires_at - now)  # Time left in seconds
        hours_left = time_left // 3600
        minutes_left = (time_left % 3600) // 60
        seconds_left = round(time_left % 60)

        expires_at_seattle = datetime.fromtimestamp(expires_at, tz=timezone('US/Pacific'))

        print("No need to refresh the token, but we will do it next if needed!")
        print(f"It has {hours_left} hours, {minutes_left} minutes, and {seconds_left} seconds left till it needs a refresh!")
        print(f"It will expire at {expires_at_seattle} (PST timezone).")

    # Update .env file
    with open('.env', 'w') as file:
        file.write(f"STRAVA_CLIENT_ID={os.getenv('STRAVA_CLIENT_ID')}\n")
        file.write(f"STRAVA_CLIENT_SECRET={os.getenv('STRAVA_CLIENT_SECRET')}\n")
        file.write(f"STRAVA_REFRESH_TOKEN={os.getenv('STRAVA_REFRESH_TOKEN')}\n")
        file.write(f"STRAVA_ACCESS_TOKEN={os.getenv('STRAVA_ACCESS_TOKEN')}\n")
        file.write(f"STRAVA_TOKEN_EXPIRES_AT={os.getenv('STRAVA_TOKEN_EXPIRES_AT')}\n")
        file.write(f"STRAVA_LAST_CHECKED={strava_last_checked} ({strava_last_checked_seattle})\n")  # Add human-readable timestamp

check_token()  # Check and update the token