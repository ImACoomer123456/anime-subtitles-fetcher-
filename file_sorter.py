import os
import shutil
import re

# Define the directory where your files and folders are located
directory = r"D:\Projects\anime subtitles fetcher\subtitles"

# Regular expression to find episode numbers in filenames
episode_regex = re.compile(r'S01E(\d{2})')

# Iterate over all items in the directory
for item in os.listdir(directory):
    item_path = os.path.join(directory, item)
    
    # Check if the item is a directory
    if os.path.isdir(item_path):
        # List all files in the directory
        for file in os.listdir(item_path):
            file_path = os.path.join(item_path, file)
            
            # If the file is an .nfo file, remove it
            if file.endswith('.nfo'):
                os.remove(file_path)
                print(f"Removed .nfo file: {file_path}")
            else:
                # Extract episode number from the filename
                match = episode_regex.search(file)
                if match:
                    episode_number = match.group(1)
                    
                    # Define the target folder based on episode number
                    target_folder = os.path.join(directory, f'Episode_{episode_number}')
                    
                    # Create the target folder if it doesn't exist
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    
                    # Move the file to the target folder
                    shutil.move(file_path, os.path.join(target_folder, file))
                    print(f"Moved file: {file_path} to folder: {target_folder}")

print("Processing complete.")
