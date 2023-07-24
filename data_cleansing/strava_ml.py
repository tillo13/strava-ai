import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from termcolor import colored
import numpy as np


folder = './data_cleansing/activities'
files = os.listdir(folder)

data_list = []
for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            try:
                data = json.load(file)
                data_dict = {
                    'average_speed': data.get('average_speed'),
                    'max_speed': data.get('max_speed'),
                    'average_cadence': data.get('average_cadence'),
                    'average_watts': data.get('average_watts'),
                    'kilojoules': data.get('kilojoules'),
                    'moving_time': data.get('moving_time'),
                    'total_elevation_gain': data.get('total_elevation_gain'),
                    'kudos_count': data.get('kudos_count'),
                    'max_watts': data.get('max_watts'),
                    'weighted_average_watts': data.get('weighted_average_watts'),
                    'suffer_score': data.get('suffer_score'),
                    'average_heartrate': data.get('average_heartrate')
                }
                
                if not any(v is None for v in data_dict.values()):
                    data_list.append(data_dict)
                    
            except (KeyError, ValueError, UnicodeDecodeError) as e:
                continue

if not data_list:
    raise ValueError("No data found in the provided files.")

dataset = pd.DataFrame(data_list)

# Dropping any rows with missing values
dataset = dataset.dropna()

features = dataset[['average_speed', 'max_speed', 'average_cadence', 'average_watts', 'kilojoules', 'moving_time', 'total_elevation_gain', 'kudos_count', 'max_watts', 'weighted_average_watts', 'suffer_score']]
labels = dataset['average_heartrate']

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2)

print('Linear Regression Results:')
model = LinearRegression()
model.fit(features_train, labels_train)

labels_pred = model.predict(features_test)

print(colored(f'R-squared: {r2_score(labels_test, labels_pred)}', 'green'))
print(colored(f'MSE: {mean_squared_error(labels_test, labels_pred)}', 'blue'))

print('\nRandom Forest Regressor Results:')
model = RandomForestRegressor(n_estimators=100)
model.fit(features_train, labels_train)
labels_pred = model.predict(features_test)

print(colored(f'R-squared: {r2_score(labels_test, labels_pred)}', 'green'))
print(colored(f'MSE: {mean_squared_error(labels_test, labels_pred)}', 'blue'))