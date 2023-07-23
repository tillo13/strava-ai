import json
import os
import glob
from collections import defaultdict

folder = './data_cleansing/activities'  
files = glob.glob(os.path.join(folder, '*.json'))

def validate_files(files):
    field_counts = defaultdict(lambda: defaultdict(int))
    file_count = len(files)
     
    for file in files:
        with open(file, 'r') as f:
            json_data = json.load(f)
            for field in json_data.keys():
                field_counts[field]['count'] += 1
    
    print(f"Number of files processed: {file_count}\n")
    print("Frequency of Field Appearance:")
    
    for field, sub_dict in field_counts.items():
        print(f"'{field}': Exists in {sub_dict['count']} files ({sub_dict['count']/file_count:.2%})")
    
    missing_fields = [field for field in field_counts if field_counts[field]['count'] < file_count]

    if missing_fields:
        print("\nFields missing in some files:")
        for field in missing_fields:
            print(f"'{field}': Missing in {file_count - field_counts[field]['count']} files ({(file_count - field_counts[field]['count'])/file_count:.2%})")
    else:
        print("\nNo missing fields found.")
    
validate_files(files)