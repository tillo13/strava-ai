import json
import pandas as pd
import os
import glob
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from scipy import stats

# This removes any anomalies from the top and bottom of the data that may skew averages.  0.05 will trim the top and bottom 5% of data for example.
TRIM_VALUE = 0.002

# These are the fields we think are important in a rider's effort
numeric_fields = {
    "distance": None,
    "moving_time": None,
    "average_speed": None,
    "average_watts": None,
    "max_watts": None,
    "suffer_score": None
}

categorical_fields = {
    "sport_type": None
}

fields = {**numeric_fields, **categorical_fields}

folder = '/activities'  
files = glob.glob(os.path.join(folder, '*.json'))

def trimmed_info(data, proportion_trimmed):
    sorted_data = np.sort(data)
    lower_trim_index = int(np.floor(proportion_trimmed * len(sorted_data)))
    upper_trim_index = int(np.ceil((1 - proportion_trimmed) * len(sorted_data)))
    trimmed_data = sorted_data[lower_trim_index:upper_trim_index]
    lower_trimmed_data = sorted_data[:lower_trim_index]
    upper_trimmed_data = sorted_data[upper_trim_index:]
    return trimmed_data, lower_trimmed_data, upper_trimmed_data

data_list = []
missing_files = 0
for file in files:
    with open(file, 'r') as f:
        json_data = json.load(f)
        if any(field not in json_data for field in fields.keys()):
            missing_files += 1  
            continue  
        single_row = {}
        for field_name, missing_value in fields.items():
            single_row[field_name] = json_data.get(field_name, missing_value)
        
        data_list.append(single_row)

if missing_files > 0:
    print(f"{missing_files} files were skipped due to incomplete data.")
else:
    print("No files were skipped as all had complete data.")

df = pd.DataFrame(data_list)
df["moving_time"] = df["moving_time"]/60

for field_name in numeric_fields:
    df[field_name].fillna(df[field_name].mean(), inplace=True)

required_columns = ['distance', 'average_speed', 'moving_time', 'average_watts']
if any(column not in df for column in required_columns):
    print("Could not find all necessary columns in data.")
    exit()

def predict_watts(df, num_clusters=3):
    model = None

    # Cluster the moving_time data
    kmeans = KMeans(n_clusters=num_clusters, n_init=10)

    df['moving_time_cluster'] = kmeans.fit_predict(df['moving_time'].values.reshape(-1, 1))

    predictions = {}
    for cluster in range(num_clusters):
        # Select instances that belong to the current cluster
        temp_df = df[df['moving_time_cluster'] == cluster]
      
        # Train linear regression 
        X = temp_df['moving_time'].values.reshape(-1,1)
        y = temp_df['average_watts']
        model = LinearRegression().fit(X, y)

        # Predict for each 10 minute interval in the cluster's ride length range
        min_ride_length = temp_df['moving_time'].min()
        max_ride_length = temp_df['moving_time'].max()

        for prediction_minute in np.arange(10, max_ride_length, 10):
            predictions[(cluster, prediction_minute)] = model.predict(np.array([prediction_minute]).reshape(-1,1))[0]

    return predictions, kmeans.cluster_centers_

predictions, cluster_centers = predict_watts(df)

activity_counts = df['sport_type'].value_counts()
print("Activity Type Counts:")
print(activity_counts)

print(f"We analysed {len(df)} of your last rides.")
print(f"From that {len(df)} rides here is some data:")
print(f"You average {df['distance'].mean() * 0.000621371:.2f} miles per ride.")

# Calculate 10% trimmed mean of speeds
average_speed, lower_trimmed_speeds, upper_trimmed_speeds = trimmed_info(df['average_speed'], TRIM_VALUE)
print(f"You average speed is {average_speed.mean() * 2.237:.2f} mph.")
print(f"This leaves out the fastest {len(upper_trimmed_speeds)} and slowest {len(lower_trimmed_speeds)} rides.")
print(f"The fastest speeds trimmed are: {upper_trimmed_speeds * 2.237}")
print(f"The slowest speeds trimmed are: {lower_trimmed_speeds * 2.237}")

# Calculate TRIM_VALUE% trimmed mean of ride times
average_time, lower_trimmed_times, upper_trimmed_times = trimmed_info(df['moving_time'], TRIM_VALUE)
print(f"Your average ride time (trimmed {TRIM_VALUE*100}%) is {average_time.mean():.2f} minutes.")
print(f"This leaves out the longest {len(upper_trimmed_times)} and shortest {len(lower_trimmed_times)} rides.")
print(f"The longest times trimmed are: {upper_trimmed_times}")
print(f"The shortest times trimmed are: {lower_trimmed_times}")

print(f"Your average watts is {df['average_watts'].mean():.2f}W (this is what we'll gauge as an average ride).")
print(f"Therefore, in the future to get to your {df['average_watts'].mean():.2f}W average ride, based on your past {len(df)} times:")

for cluster, cluster_center in enumerate(cluster_centers):
    print(f"For a ride length around {cluster_center[0]:.2f} minutes:")
    min_ride_length = 10
    max_ride_length = min(df[df['moving_time_cluster'] == cluster]['moving_time'].max(), cluster_center[0] + 10)
    for prediction_minute in np.arange(min_ride_length, max_ride_length, 10):
        print(f"You'd need to have your average_watts be {predictions[(cluster, prediction_minute)]:.2f} by minute {prediction_minute}, and you should try to hit those marks.")