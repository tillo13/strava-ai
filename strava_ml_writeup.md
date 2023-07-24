# Delving Deep into Strava Workouts with Python and Machine Learning

Over the weekend, I thought I'd dig around into my repository of ~2000 workouts on Strava (https://www.strava.com/athletes/18443678) with the idea to study, explore, and unlock some fun insights with Machine Learning (ML). This writeup will narrate my explorations, shedding light on how different stages of machine learning can be harnessed to extract value from raw data. I performed data extraction, processing, exploration, modeling, evaluation, and ultimately prediction, leveraging Python.

## The First Milestone: Channeling Strava Data Into Our System - An Enhanced Walking Through

Accumulating the raw Strava data was a challenge that I was prepared to take on. What procedure was adopted to accomplish this? Very simple. I utilized the power of Python and some of its libraries to extract data from the Strava API and then stored it in a proper format, allowing easy data management and further processing. Let's delve a bit deeper into the mechanics of this.

To begin with, the Python requests library was instrumental in connecting to the Strava API and retrieving my activity data. The access token, which authenticates our application and allows the API to recognize who we are, was first acquired through the check_token() function from initialize.py.

Here's a more extensive look at initialize.py, the script that makes the first few strides towards our data extraction journey.

```python
...
# Get the latest access token
access_token = check_token()

# Setup the API call
url = "https://www.strava.com/api/v3/athlete/activities"
headers = {'Authorization': f'Bearer {access_token}'}
params = {'per_page': 7, 'page': 1}

# Send the GET request
response = requests.get(url, headers=headers, params=params)

...
```
Going forward, the last_n_activities.py script deals with the task of obtaining the Strava activity data. In this script, we use the requests.get() method and supply it with the API endpoint URL, our headers (which includes the access token), and additional parameters that specify the number of activities per page and the page number.

The response from the API call is a JSON object, which we then decode using response.json(). If the API response can be successfully decoded, we continue by saving it into individual JSON files.

```python
...
# Get the JSON response
activities = response.json()

# Create a new directory to store our files
folder_path = './activities'
os.makedirs(folder_path, exist_ok=True)
existing_files = os.listdir(folder_path)

# Save each activity data into separate JSON files
num_duplicates = 0
num_new_activities = 0
...
for activity in activities:
    activity_id = activity['id']
    file_path = os.path.join(folder_path, f'{activity_id}.json')

    if f'{activity_id}.json' in existing_files:
        num_duplicates += 1
        continue
    
    with open(file_path, 'w') as file:
        json.dump(activity, file, indent=4)
    num_new_activities += 1

...
```
The script creates a dedicated folder named 'activities' to store each JSON file. To ensure the folder does not get flooded with duplicate files, we perform a simple check if the current activity's JSON file already exists in the folder directory before proceeding to write the file. Thus, this Python magic accomplishes the major step of localizing my raw data for the analysis stages that follow.

## Sorting the Raw Data: Field Frequency and Missing Fields

After pulling my raw Strava data, the focus of this stage was to sort and organize the data. More precisely, I was interested in determining the frequency of occurrence of different fields or data points across the ~2000 Strava workouts represented as JSON files. 

```python
folder = './data_cleansing/activities'  
files = glob.glob(os.path.join(folder, '*.json'))

def validate_files(files):
    field_counts = defaultdict(lambda: defaultdict(int))
    file_count = len(files)
...
for file in files:
    with open(file, 'r') as f:
        json_data = json.load(f)
        for field in json_data.keys():
            field_counts[field]['count'] += 1
...
print(f"Number of files processed: {file_count}")
...
print('Frequency of Field Appearance:')
for field, data in field_counts.items():
    percentage = data['count'] / file_count * 100
    print(f"'{field}': Exists in {data['count']} files ({percentage:.2f}%)")
...
print('Fields missing in some files:')
for field, data in field_counts.items():
    if data['count'] != file_count:
        missing_count = file_count - data['count']
        missing_percentage = missing_count / file_count * 100
        print(f"'{field}': Missing in {missing_count} files ({missing_percentage:.2f}%)")
```
This exercise proves beneficial in understanding the distribution of data available across the different fields, such as 'resource_state', 'athlete', and many others that were appearing in 100% of files.

## Diving Deeper: Classifying Data by Platforms

The uniqueness of certain workout events lies in the platform used to record each activity. This stage of data exploration drills down into exercise data classification based on the recording platform. For this purpose, a Python script named strava_activity_classification.py forms the backbone of the process. 

```python
import os
import json

folder = './data_cleansing/activities'
files = os.listdir(folder)
...
peloton_activities = {'Ride': 0, 'Yoga': 0, 'EBikeRide': 0, 'Run': 0, 'Walk': 0, 'Workout': 0, 'Other': 0}
...
for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            data = json.load(file)
...
external_id = data.get('external_id')
trainer = data.get('trainer', False)
activity_type = data.get('type')
sport_type = data.get('sport_type')
...
if external_id is not None and external_id.endswith('.tcx') and len(external_id) == 36:
    if trainer and not start_latlng and not end_latlng:
        if activity_type in peloton_activities.keys() and sport_type == activity_type:
            peloton_activities[activity_type] += 1
        else: 
            peloton_activities['Other'] += 1
        continue
...
```
In the end, the script prints out a statistical summary of each type of workout for each platform, giving a clear picture of the proportion of my workouts being performed on various platforms.

## Highlighting the Heroes: Top Rides

One particularly thrilling adventure was the design and deployment of a specialized scoring system for my cycling endeavors on the Peloton platform. The Briskr score offered a numerical representation of the accomplishments in cycling.

```python
def calculate_score(data):
    return data['kilojoules']
...

for filename in files:
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        ...
        score = calculate_score(data)
        peloton_ride_scores.setdefault(ride_category, {})[filename] = score
        ...

categories_order = [5, 10, 15, 20, 30, 45, 60, 75, 90] 
sorted_peloton_ride_scores = {k: peloton_ride_scores[k] for k in categories_order if k in peloton_ride_scores}
...
print('\n' + colors[idx] + f'Top rides for {category} mins:' + Style.RESET_ALL)
headers = ["Mins", "Ride Date", "kJ Score", "Avg Speed(mph)", "Distance(miles)", "Avg Watts", "kJ/min", "Kudos Count", "Filename", "Ride Name"] 
print(tabulate(table, headers=headers))
...
```
The charted journey through my cycling activities was rife with explorations, inspiring me and hopefully inspiring others to keep pedaling harder.

## Timing Meticulously: Classification of Workouts

To illustrate the chronology of fitness routines and to identify when these routines typically occur, the Python script written to segment workouts according to the respective scheduling was titled `when_you_workout.py`.

```python
...
for filename in files:
    with open(os.path.join(folder, filename), 'r') as file:
        data = json.load(file)
...
        custom_time = start_datetime.astimezone(custom_tz)
        workouts_per_hour[custom_time.hour] += 1
...
attrs = ['max_heartrate', 'average_heartrate', 'kilojoules', 'weighted_average_watts', 'max_watts', 'average_watts', 'average_cadence', 'max_speed', 'average_speed', 'elapsed_time', 'distance']
attr_values = defaultdict(lambda: defaultdict(list))
... 
for attr in attrs:
    value = data.get(attr)
    if value is not None and value != 0:
        if attr == 'elapsed_time':
            value /= 60
        elif attr == 'distance':
            value /= 1609.34
        elif 'speed' in attr:
            value *= 2.23694  # Convert to miles per hour
        attr_values[custom_time.hour][attr].append(value)
...
table_data = []
...
for hour in range(24):  
    if hour in workouts_per_hour:
        count = workouts_per_hour[hour]
        averages = {attr: round(statistics.mean(remove_outliers(attr_values[hour][attr])), 2) for attr in attrs if attr_values[hour][attr]}
        row = [hour, count] + [averages.get(attr, 'N/A') for attr in attrs]
    else:
        row = [hour, 0] + ['N/A' for _ in attrs]
    table_data.append(row)

table_data = color_rows(table_data, attrs)
print(tabulate(table_data, headers=['Hour', 'Workouts'] + attrs))
```

This script aided in mapping the frequency of workouts at different times of the day.

## Breaking the Boundaries: Regression Models and Machine Learning

Next, focus turned to Machine Learning, more specifically, regression models. The aim was to ascertain how different factors influence the average heart rate during a workout.

```python
...

print('Linear Regression Results:')
model = LinearRegression()
model.fit(features_train, labels_train)
...

print('\nRandom Forest Regressor Results:')
model = RandomForestRegressor(n_estimators=100)
model.fit(features_train, labels_train)
```

I used two regression algorithms, Linear Regression and Random Forest Regressor, to make predictions based on existing workout data. The scripts also maintain a good check on the performance of the created models.

```python
...
for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            ...
if not data_list:
    raise ValueError("No data found in the provided files.")
    
dataset = pd.DataFrame(data_list)

# Dropping any rows with missing values
dataset = dataset.dropna()

...

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2)

...

labels_pred = model.predict(features_test)

print(colored(f'R-squared: {r2_score(labels_test, labels_pred)}', 'green'))
print(colored(f'MSE: {mean_squared_error(labels_test, labels_pred)}', 'blue'))
```

These activities resulted in R-squared values of 0.508 and 0.774 for Linear Regression and Random Forest Regressor, respectively.

## Conclusion

This journey proved the immense potential that arises when fitness and Machine Learning intersect. Each stage, from data extraction and cleaning to prediction, provided a firsthand look at the way patterns and insights can be detected from data. 

Two regression models, Linear Regression and Random Forests were built and used successfully in predicting the average heart rate during a workout - a feat of its own. On a technical level, I found Random Forests to deliver better accuracy and uphold robustness against overfitting.

Future possibilities include delving deeper into the data to identify outliers and skewness, employing different model architectures, and refining hyperparameters. This will go a long way in improving prediction accuracy.

Although this is an exciting first step, there is much more to be explored at the confluence of fitness and ML. This opportunity has only scratched the surface and promises a rich potential yet to be tapped into.
```