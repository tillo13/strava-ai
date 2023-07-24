# Strava Workout Analyzer + Machine Learning Exploration

Read a bit more in depth about it here: https://github.com/tillo13/strava-ai/blob/main/strava_ml_writeup.md 

This digital suite, crafted from a collection of Python scripts, is a specialized toolkit for the Strava fitness application. Its primary purpose is to download, cleanse, and perform a meticulous analysis of a user's ‘Strava activities’. It is enriched with scripts that serve a variety of utilities - connecting with the Strava API, fetching and refreshing access tokens, downloading activities, validating the reliability of JSON data, and eventually providing classified, scored, and wholesome summaries of the fitness activities.

Notably equipped for Strava data handling and analysis, the repository carries the following scripts:

1. **initialize.py**: 
Here's where the journey begins. By sending a GET request to the Strava API, this script fetches a new access token, performs checks for existing ones, validates them, and, if necessary, refreshes them. For audit and debugging purposes, all token-checking activities are duly logged.

2. **last_n_activities.py**: 
This utility script reaches out to the Strava API to retrieve the most recent activities. Each activity is downloaded, earmarked with its respective activity_id, and saved as an individual JSON file. Additionally, it ensures no activity is copied twice, preventing duplications, and storing only new additions.

3. **validate_json.py**: 
This script is tasked with validating the downloaded JSON files bearing cycling activities. It scans through each field in every file, counts their occurrences, verifies the presence of all necessary fields, and ultimately, provides a detailed transparency report.

4. **strava_activity_classification.py**: 
Resulting from this script is the systematic classification of Peloton classes. Equipped with tailored algorithms to track sub-types of generic classifications such as "Workout," it is designed to meticulously separate other platform activities, distinguishing between those logged by ELEMNT BOLT, Zwift, Garmin Ping, Strava Direct, amongst others.

5. **top_peloton_rides.py**: 
This script is your personal leaderboard maker. It navigates through your history of Peloton rides on Strava to rank your top 5 rides. The scoreboard is curated based on a scoring system that calculates the effort exerted during each ride.

6. **briskr_score.py**: 
Borrowing from the popular Bris.kr score method from the project I made for Boomi here: https://community.boomi.com/s/article/Boomi-helps-keep-you-healthy, this script evaluates the ride intensity, honoring the highest scores to the most intense rides. It nets out with a compiled summary of your top 5 rides for each ride length category, celebrating the sweat and gears of each endeavor.

7. **monthly_totals_over_time.py**: 
This script is your timeline navigator. It rummages through the downloaded activities, assorting them by activity type and month before outputting a wholesome summary. For each month, it tallies up the total number of unique activities.

## Preparation and Setup
Please follow the steps below to prepare your environment for the Strava Workout Analyzer:

1. Start by cloning this repository to your local system.
2. You'll need to create a `.env` file in the root directory.
3. Inside `.env`, include your Strava Client ID and Client Secret:

```sh
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
```
Substitute `your_client_id` and `your_client_secret` with your actual credential details.

### Internal Workings - Python Libraries Used:
Running behind the scenes of this project are the under-mentioned Python libraries:
- json
- os
- glob
- collections
- csv
- requests
- datetime
- dotenv
- pytz
- pandas
- colorama
- tabulate
- re

### How to Run these Scripts:
1. Please ensure that Python 3 is installed on your system.
2. Use pip to install the necessary Python dependencies, mentioned above, with the command `pip install <library_name>`.
3. Add your project directory to your PYTHONPATH environment variable.
4. Run the required script with the command `python <filename.py>`.

### What the Future Holds:
Hit me up with your valuable ideas for refining this project. Tentative directions where the project can expand include:
- Incorporation of a graphical interface to enhance user interaction.
- Improved activity categorization based on user input.
- Introduction of a weather interaction module, enabling score adjustments based on prevailing weather conditions.
- Enumeration of more performance evaluation metrics for further user insights.

## API Rate Limiting
Please be mindful of the restrictions imposed by Strava API. It has a limit of 100 requests per 15 minutes and 1000 requests in 24 hours. Exceeding the limit is considered unfriendly behavior towards their API!

# An Illustrated Summary through Screenshots

Take a tour of these screenshots to understand the visual outputs of the scripts.

![Top Rides](./images/top_rides.png)
![Average KJ](./images/avg_kj.png)
![Classification of Strava rides](./images/strava_activity_classification.png)
![When you workout](./images/when_you_workout.png)