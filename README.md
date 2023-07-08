# Strava API Activities Fetcher

This project is used to fetch activities from the Strava API. The project consists of 2 main files: `initialize.py` and `last_n_activities.py`. The `initialize.py` file retrieves the required access tokens for API access and checks if these tokens are valid or not. If not, it refreshes the tokens.

`last_n_activities.py` queries the Strava API for the user's recent activities, and saves each activity to a separate file. It also provides functionalities to prevent duplicate activities from being fetched (if they already exist in the output directory).

## Requirements
Python 3
Required Python packages: `csv`, `os`, `requests`, `json`, `pytz`, `dotenv`

## Setup
1. Clone this repository to your local system
2. Create a `.env` file in the same directory as `initialize.py` and `last_n_activities.py`.
3. Inside `.env`, add your Strava Client ID and Client Secret as follows:

```sh
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
```

Replace `your_client_id` and `your_client_secret` with your actual Client ID and Client Secret.

## Usage
Usage of this project is simple. Just run the following commands:

```sh
python3 initialize.py
```

The above command will check if your tokens are still valid or not and refresh them if they're expired.

```sh
python3 last_n_activities.py
```

The above command will fetch the user's last n activities from the Strava API and save each activity to a separate file.

## Limit Rate
Strava API has a limit of 100 requests per 15 minutes and 1000 requests per day. If the limit is exceeded, subsequent requests will fail.