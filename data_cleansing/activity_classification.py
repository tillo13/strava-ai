import os
import glob
import json
from collections import Counter

def analyze_files(files):
    word_counts = Counter()

    for file in files:
        with open(file, 'r') as f:
            json_data = json.load(f)
            # split the name into words and add them to the Counter
            words = json_data['name'].split()
            word_counts.update(words)
            
    return word_counts

folder = './activities'  
files = glob.glob(os.path.join(folder, '*.json'))

word_counts = analyze_files(files)

# print all words, sorted by their count in descending order
for word, count in sorted(word_counts.items(), key=lambda x: -x[1]):
    print(f"{word}: {count}")