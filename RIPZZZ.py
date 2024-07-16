import os
import subprocess
from googleapiclient.discovery import build, service_account
from google.oauth2.credentials import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload
import json


#Getting ZZZ Directory
gameDir = os.path.dirname(__file__)
ZZZ = 'ZenlessZoneZero.exe'
gamePath = os.path.join(gameDir, ZZZ)
persistFolder = os.path.join(gameDir, r'ZenlessZoneZero_Data\Persistent')

#Checking if there's a remote file
def check_word_in_filenames(word_to_check, directory):
    found_filenames = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):  # Check if it's a file
            if word_to_check.lower() in filename.lower():
                found_filenames.append(filename)
    return found_filenames


if __name__ == "__main__":
    word_to_check = "remote"  # Change this to the word you want to check
    found_files = check_word_in_filenames(word_to_check, persistFolder)
#End
#Find the specific remote files
dataFound = False
audioFound = False
resFound = False
silenceFound = False

reskeyword = "res_version_remote"
datakeyword = "data_version_remote"
audiokeyword = "audio_version_remote"
silencekeyword = "silence_version_remote"

# Check if the keyword is in any of the filenames
for filename in found_files:
    for keyword in [reskeyword, datakeyword, audiokeyword, silencekeyword]:
        if keyword in filename:
            if keyword == reskeyword:
                resFound = True
            elif keyword == datakeyword:
                dataFound = True
            elif keyword == audiokeyword:
                audioFound = True
            elif keyword == silencekeyword:
                silenceFound = True

# Print the boolean flags to verify
print("resFound:", resFound)
print("dataFound:", dataFound)
print("audioFound:", audioFound)
print("silenceFound:", silenceFound)

# Example string variable
dataRemote = ["data_revision", "data_version_persist"]
audioRemote = ["audio_revision", "audio_version_persist"]
resRemote = ["res_revision", "res_version_persist"]
silenceRemote = ["silence_revision", "silence_version_persist"]

# Initialize RemoteFiles as an empty list
persistFiles = []

# Check if the boolean condition is true
if dataFound:
    persistFiles.extend(dataRemote)
    data_path = os.path.join(persistFolder, datakeyword)
    os.remove(data_path)
    print(f'Deleted: {datakeyword}')
if audioFound:
    persistFiles.extend(audioRemote)
    audio_path = os.path.join(persistFolder, audiokeyword)
    os.remove(audio_path)
    print(f'Deleted: {audiokeyword}')
if resFound:
    persistFiles.extend(resRemote)
    res_path = os.path.join(persistFolder, reskeyword)
    os.remove(res_path)
    print(f'Deleted: {reskeyword}')
if silenceFound:
    persistFiles.extend(silenceRemote)
    silence_path = os.path.join(persistFolder, silencekeyword)
    os.remove(silence_path)
    print(f'Deleted: {silencekeyword}')

# Print RemoteFiles to see the result
print(persistFiles)
#End
#Download from GDrive
# Path to the service account key file
service_account_file = r'D:\Games\ripzzz-429515-fd3104418c05.json'

# Initialize the Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

credentials = service_account.Credentials.from_service_account_file(
    service_account_file, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def downloadPersist(folder_id, file_names, destination_folder):
    try:
        # List files in the folder
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields='files(id, name)'
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            print('No files found.')
        else:
            print('Files:')
            for file in files:
                file_id = file.get('id')
                file_name = file.get('name')
                if file_name in file_names:
                    print(f'Downloading {file_name}...')
                    
                    # Download the file
                    request = service.files().get_media(fileId=file_id)
                    fh = io.FileIO(f'{destination_folder}/{file_name}', 'wb')
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    
                    print(f'{file_name} downloaded successfully.')
    
    except Exception as e:
        print(f'An error occurred: {e}')

folder_id = '1MxQlcIX0EdOSUQKfslxIAMcWJS7GEgUK'
file_names_to_download = persistFiles  # Specify the filenames you want to download
destination_folder = persistFolder
#End


#RunZZZ
def runZZZ():
    subprocess.run([gamePath])
#End
#calls

downloadPersist(folder_id, file_names_to_download, destination_folder)
runZZZ()
