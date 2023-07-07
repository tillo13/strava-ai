import requests
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('STRAVA_CLIENT_ID')
client_secret = os.getenv('STRAVA_CLIENT_SECRET')

# Replace this with your authorization code
authorization_code = '10b5ae228b3a7023dec7e69b2d2c2f478a0b2cec' 

url = 'https://www.strava.com/oauth/token'

data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': authorization_code,
    'grant_type': 'authorization_code'
}

response = requests.post(url, data=data)

print(response.json())
