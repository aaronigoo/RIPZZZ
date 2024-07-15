import os
import requests
from datetime import datetime
import atexit
import subprocess

#Checking if there's a remote file

def checkRemote(word_to_check, directory):
    found_filenames = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if word_to_check.lower() in filename.lower():
                found_filenames.append(filename)
    return found_filenames

# Example usage:
if __name__ == "__main__":
    directory_path = '/path/to/your/directory'  # Replace with your directory path
    word_to_check = "report"  # Change this to the word you want to check
    
    found_files = checkRemote(word_to_check, directory_path)
    
    if found_files:
        print(f"Files containing '{word_to_check}' in {directory_path}:")
        for filename in found_files:
            print(filename)
    else:
        print(f"No files found containing '{word_to_check}' in {directory_path}.")

#Download from Github


def download_file_from_github(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        # Check if local file exists and get its last modified timestamp
        file_exists = os.path.exists(save_path)
        local_last_modified = os.path.getmtime(save_path) if file_exists else 0
        
        # Parse GitHub's last modified timestamp
        github_last_modified_str = response.headers.get('Last-Modified')
        github_last_modified = datetime.strptime(github_last_modified_str, '%a, %d %b %Y %H:%M:%S %Z') if github_last_modified_str else None
        
        # Compare timestamps and download if GitHub version is newer
        if not file_exists or (github_last_modified and github_last_modified.timestamp() > local_last_modified):
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully: {save_path}")
        else:
            print(f"File '{save_path}' is already up to date.")
    else:
        print(f"Failed to download file, status code: {response.status_code}")

# Example usage:
if __name__ == "__main__":
    github_url = 'https://raw.githubusercontent.com/username/repository/branch/path/to/file'
    save_path = '/path/to/save/directory/downloaded_file.txt'

    download_file_from_github(github_url, save_path)


#Run ZenlessZoneZero when exiting script

def runZZZ():
    # Replace with the command or application you want to run
    subprocess.run(["/path/to/your/application"])  # Example command to run an application

# Registering the function to run before exit
atexit.register(runZZZ)

