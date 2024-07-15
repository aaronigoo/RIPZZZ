import os
import requests
from datetime import datetime
import atexit
import subprocess

#Getting ZZZ Directory

# Get the directory path of the current script
script_dir = os.path.dirname(__file__)

# Specify the filename you want to access (example: 'example.txt')
filename = 'ZenlessZoneZero.exe'

# Construct the full path to the file
file_path = os.path.join(script_dir, filename)

# Check if the file exists before accessing it
if os.path.exists(file_path):
    # Open the file and read its contents (example: read mode 'r')
    with open(file_path, 'r') as file:
        file_contents = file.read()
        print(f"Contents of '{filename}':\n{file_contents}")
else:
    print(f"File '{filename}' not found in directory: {script_dir}")

#End
#Checking if there's a remote file

def checkRemote(RemoteFile, directory):
    found_filenames = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if word_to_check.lower() in filename.lower():
                found_filenames.append(filename)
    return found_filenames

# Example usage:
if __name__ == "__main__":
    directory_path = '/path/to/your/directory'  # Replace with your directory path
    RemoteFile = "Remote"  # Change this to the word you want to check
    
    found_files = checkRemote(RemoteFile, directory_path)
    
    if found_files:
        print(f"Files containing '{RemoteFile}' in {directory_path}:")
        for filename in found_files:
            print(filename)
    else:
        print(f"No files found containing '{RemoteFile}' in {directory_path}.")

#End
#Download from Github

def downloadPersistFiles(url, save_path):
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

    downloadPersistFiles(github_url, save_path)

#End
#Run ZenlessZoneZero when exiting script

def runZZZ():
    # Replace with the command or application you want to run
    subprocess.run([file_path])  # Example command to run an application

# Registering the function to run before exit
atexit.register(runZZZ)

