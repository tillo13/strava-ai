import os
import json
from tabulate import tabulate
from colorama import Fore, Style
from datetime import datetime
import re

#add other values here if you want to change up the scoring
def calculate_score(data):
    return data['kilojoules']

def extract_time_from_name(name):
    duration_match = re.search("(\d+)\smin", name)
    return int(duration_match.group(1)) if duration_match else None

def format_ride_time(ride_time):
    datetime_object = datetime.strptime(ride_time, '%Y-%m-%dT%H:%M:%SZ') 
    formatted_string = datetime_object.strftime('%Y-%B-%d')
    return formatted_string

def categorize_ride(data):
    duration = data['elapsed_time'] / 60  # duration in minutes
    expected_duration = extract_time_from_name(data['name'])
    # the ride will be categorized only if name duration and actual duration are almost the same (with some error tolerance, you can change it)
    if expected_duration and abs(duration - expected_duration) <= 2:
        return expected_duration
    return None

directory = './data_cleansing/activities'
files = os.listdir(directory)
peloton_ride_scores = {}

for filename in files:
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r') as file:
            data = json.load(file)

            try:
                external_id = data.get('external_id')
                trainer = data.get('trainer', False)
                activity_type = data.get('type')
                sport_type = data.get('sport_type')

                if (external_id is not None and external_id.endswith('.tcx') and len(external_id) == 36 and trainer and activity_type == 'Ride' and sport_type == 'Ride'):
                    ride_category = categorize_ride(data)
                    if ride_category is not None:
                        score = calculate_score(data)
                        peloton_ride_scores.setdefault(ride_category, {})[filename] = score

            except (KeyError, TypeError) as e:
                continue

categories_order = [5, 10, 15, 20, 30, 45, 60, 75, 90] 
sorted_peloton_ride_scores = {k: peloton_ride_scores[k] for k in categories_order if k in peloton_ride_scores}

colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.RED, Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX]

for idx, (category, rides) in enumerate(sorted_peloton_ride_scores.items()):
    sorted_rides = sorted(rides.items(), key=lambda x: x[1], reverse=True)
    #want to see the worst rides?  Uncomment this line -> sorted_rides = sorted(rides.items(), key=lambda x: x[1])
    table = []

    for filename, score in sorted_rides[:5]:
        with open(os.path.join(directory, filename), 'r') as file:
            data = json.load(file)
        
        ride_time = format_ride_time(data.get('start_date_local', 'N/A'))
        average_speed = data.get('average_speed', 'N/A') * 2.237 if data.get('average_speed') else 'N/A'  # km/h to miles/h
        total_distance = data.get('distance', 'N/A') / 1609 if data.get('distance') else 'N/A' # meter to mile
        average_watts = data.get('average_watts', 'N/A')        
        kudos_count = data.get('kudos_count', 'N/A')
        kj_per_min = score / category if category != 0 else 'N/A' # add new metric kj/min
        ride_name = data.get('name', 'N/A')

        table.append([category, ride_time, score, average_speed, total_distance, average_watts, kj_per_min, kudos_count, filename, ride_name]) #update table append
    
    print('\n' + colors[idx] + f'Top rides for {category} mins:' + Style.RESET_ALL)
    headers = ["Mins", "Ride Date", "kJ Score", "Avg Speed(mph)", "Distance(miles)", "Avg Watts", "kJ/min", "Kudos Count", "Filename", "Ride Name"] #update headers
    print(tabulate(table, headers=headers))