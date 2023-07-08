import csv
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from os.path import isfile
import pytz
import json


load_dotenv()

url_csv = "access_tokens.csv"
url_check = "token_check_log.csv"

def convert_timestamp(timestamp):
    timezone = pytz.timezone('America/Los_Angeles')  # Set the timezone to Seattle, WA
    local_time = datetime.fromtimestamp(timestamp, tz=timezone)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

def get_athlete_id(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get('https://www.strava.com/api/v3/athlete', headers=headers)
    status_code = response.status_code

    if status_code == 200:
        return status_code, response.json()
    else:
        print(f'Error fetching athlete data. Status code: {status_code}')
        return status_code, None

def check_for_id(client_id):
    if not isfile(url_csv):
        return False
    with open(url_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['client_id'] == client_id:
                return True
    return False

def get_refresh_token(client_id):
    if check_for_id(client_id):  # Check if the CSV file exists
        with open(url_csv, 'r') as file:
            reader = csv.DictReader(file)
            for row in reversed(list(reader)):  # Start from the end and move up
                if row['client_id'] == client_id:
                    return row['refresh_token']
    return os.getenv('INITIAL_STRAVA_REFRESH_TOKEN')  # Return initial refresh token if CSV does not exist

def get_new_token():
    url = "https://www.strava.com/oauth/token"
    client_id = os.getenv('STRAVA_CLIENT_ID')
    refresh_token = get_refresh_token(client_id)
    
    payload = {
        'client_id': client_id,
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'f': 'json'
    }

    try:
        response = requests.post(url, params=payload)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    except requests.exceptions.RequestException as err:
        print (err)
        return None, None  # Return None if any error occurs during request

    response_json = response.json()

    file_exists = isfile(url_csv)
    
    with open(url_csv, mode='a') as file:
        headers = ['client_id', 'access_token', 'expires_at', 'refresh_token']
        writer = csv.DictWriter(file, fieldnames=headers)
        
        if not file_exists:  # If it's the first time and the file does not exist
            writer.writeheader()

        if not check_for_id(client_id):  # Check if the ID does not exist
            writer.writerow({
                'client_id': client_id, 
                'access_token': response_json['access_token'], 
                'expires_at': response_json['expires_at'], 
                'refresh_token': response_json['refresh_token']
            })

    print("Strava response:", response_json)  # Print the response
    return response_json['access_token'], response_json['refresh_token']


def check_token():
    client_id = os.getenv('STRAVA_CLIENT_ID')

    print("Getting new access token...")
    access_token, refresh_token = get_new_token()
    if access_token is None and refresh_token is None:
        return

    # Call get_athlete_id and get the response
    status_code, response_data = get_athlete_id(access_token)
    print(f'get_athlete_id response: Status code: {status_code}')
    print(json.dumps(response_data, indent=4))  # Print the full JSON response







    
    with open(url_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reversed(list(reader)):  # Start from the end and move up
            if row['client_id'] == client_id:
                expires_at = row['expires_at']

    now = datetime.now()
    human_readable_timestamp = convert_timestamp(now.timestamp())

    result = "No refresh needed"
    if now.timestamp() > int(expires_at):
        print("Token has expired! Refreshing token...")
        access_token, refresh_token = get_new_token()
        result = "Token refreshed"
        print("Token has been refreshed!")

    file_exists = isfile(url_check)
    with open(url_check, mode='a') as file:
        headers = ['client_id', 'token_last_checked', 'human_readable_timestamp', 'result']
        writer = csv.DictWriter(file, fieldnames=headers)
        
        if not file_exists:  # If it's the first time and the file does not exist
            writer.writeheader()

        writer.writerow({
            'client_id': client_id,
            'token_last_checked': now.timestamp(),
            'human_readable_timestamp': human_readable_timestamp,
            'result': result
        })

    return access_token

if __name__ == "__main__":
    check_token()