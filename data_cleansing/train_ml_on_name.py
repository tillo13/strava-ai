from collections import defaultdict
import json
import glob
import os

# define keywords for each activity
keywords = {
    'cycling': ['ride', 'cycling', 'biking'],
    'yoga': ['yoga', 'meditation'],
    'strength': ['strength', 'arms', 'weight'],
    # add more categories as needed
}

# counter dict
summary = defaultdict(int)

# scan all files
folder = './data_cleansing/activities'  
files = glob.glob(os.path.join(folder, '*.json'))

for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        name = data['name'].lower()  # transform name to lowercase to avoid case mismatch
    
    # check each category
    for category, kwds in keywords.items():
        if any(kwd in name for kwd in kwds):
            summary[category] += 1
            print(f"'{data['name']}' is classified as '{category}'")
            break  # a file belongs to first matched category
    else:  # use for...else to handle no-matched case
        summary['unknown'] += 1
        print(f"'{data['name']}' couldn't be classified")

print("\nFile Category Summary:")
for category, count in summary.items():
    print(f"{category} : {count}")