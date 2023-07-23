import os
import json
from collections import defaultdict
from datetime import datetime
import numpy as np
from sklearn.cluster import KMeans

folder = './data_cleansing/activities'
files = os.listdir(folder)
total_activities_by_type = defaultdict(int)
activity_likes_by_type = defaultdict(int)  # Store 'likes' for each activity
activity_counts_by_month = defaultdict(lambda: defaultdict(int))
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for filename in files:
    if filename.endswith('.json'):
        with open(os.path.join(folder, filename), 'r') as file:
            data = json.load(file)

            try:
                start_date = datetime.strptime(data["start_date"], "%Y-%m-%dT%H:%M:%SZ")
                month_key = start_date.strftime("%Y-%m")

                activity_type = data.get('type')
                activity_likes = data.get('likes', 0)  # Assuming 'likes' are available in the data

                activity_counts_by_month[month_key][activity_type] += 1
                total_activities_by_type[activity_type] += 1
                activity_likes_by_type[activity_type] += activity_likes

            except (KeyError, TypeError):
                continue

total_months = len(activity_counts_by_month)
    
weekly_avg_activities = {activity: total / total_months / 4 for activity, total in total_activities_by_type.items()}
activity_names = list(weekly_avg_activities.keys())
activity_counts = np.array(list(weekly_avg_activities.values())).reshape(-1, 1)

kmeans = KMeans(n_clusters=3, random_state=0).fit(activity_counts)

activity_cluster_labels = dict(zip(activity_names, kmeans.labels_))
activity_cluster_centers = dict(zip(range(3), [center[0] for center in kmeans.cluster_centers_]))

# Sort activities in each cluster by 'likes' in descending order
sorted_activities = []
for cluster in range(3):
    activities_in_cluster = [k for k, v in activity_cluster_labels.items() if v == cluster]
    sorted_activities += sorted(activities_in_cluster, key=lambda k: activity_likes_by_type[k], reverse=True)

# Recommend a daily workout based on sorted activities
recommended_workout = {}
for i, day in enumerate(days_of_week):
    recommended_activity = sorted_activities[i % len(sorted_activities)]
    recommended_workout[day] = recommended_activity

print(recommended_workout)