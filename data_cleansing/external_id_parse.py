import os
import json

folder = './activities'
files = os.listdir(folder)

# Initialize dictionaries to store file types and their counts
file_types = {}
file_types_with_trainer_true = {}
file_types_with_trainer_and_latlng = {}

# Initialize list to store mismatched external_ids
mismatched_ids = []

# Loop through each file in the directory
for filename in files:
    # Check if the file is a json file to avoid reading non-json files
    if filename.endswith('.json'):
        # Open the file
        with open(os.path.join(folder, filename), 'r') as file:
            # Load the json content
            data = json.load(file)

            try:
                external_id = data.get('external_id')
                trainer = data.get('trainer', False)  # get 'trainer' field (default to false if it does not exist)
                
                # Check if start_latlng and end_latlng exist and are empty
                start_latlng = data.get('start_latlng', [])
                end_latlng = data.get('end_latlng', [])
                
                # Check if external_id exists and is not None
                if external_id is not None:
                    file_extension = os.path.splitext(external_id)[1]
                    if file_extension:  # Check if there's a file extension
                        # Increment the extension count
                        file_types[file_extension] = file_types.get(file_extension, 0) + 1
                        # Increment the count in trainer true or false dictionary
                        if trainer:
                            file_types_with_trainer_true[file_extension] = file_types_with_trainer_true.get(file_extension, 0) + 1
                            # Check if latlng values are empty
                            if not start_latlng and not end_latlng:
                                # Increment count for files with trainer=true and empty latlng values
                                file_types_with_trainer_and_latlng[file_extension] = file_types_with_trainer_and_latlng.get(file_extension, 0) + 1
                    else:
                        mismatched_ids.append(external_id)
                else:
                    mismatched_ids.append(external_id)

            except (KeyError, TypeError) as e:
                continue

# Print number of files found for each file type
print("Searching ONLY the EXTERNAL_ID field:")
for file_type, count in file_types.items():
    print(f'Found {count} files with {file_type} type')

# Print the mismatched external_ids
print("\nMismatched external_ids:")
for id in set(mismatched_ids):  # using set to avoid duplicate entries
    print(id)

print("\nSearching EXTERNAL_ID and THEN trainer=true")
# Print number of files found for each file type with trainer=true
for file_type, count in file_types_with_trainer_true.items():
    print(f'Found {count} files with {file_type} type AND trainer=true')

print("\nSearching EXTERNAL_ID and THEN trainer=true and THEN lat/long=null")
# Print number of files found for each file type with trainer=true and empty latlng values
for file_type, count in file_types_with_trainer_and_latlng.items():
    print(f'Found {count} files with {file_type} type, trainer=true, and start/end lat/long=null')