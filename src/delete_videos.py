import os
import re

# Specify the directory path
directory = 'outputs/videos'

# List all files in the directory
files = os.listdir(directory)

# Define a regular expression pattern to match filenames ending with a number
pattern = re.compile(r'_[0-9]')

# Iterate through the files
for file in files:
    # Check if the file name matches the pattern
    if pattern.search(file):
        # Construct the full file path
        file_path = os.path.join(directory, file)
        
        # Delete the file
        os.remove(file_path)
        print(f"Deleted: {file_path}")