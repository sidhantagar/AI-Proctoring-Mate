import os
import requests
from google_drive_downloader import GoogleDriveDownloader as gdd

SHORTNER = 'http://bit.ly/'
code = '3uibkub'

r = requests.get(SHORTNER+code)


url = r.url
for i in url.split('/'):
    if len(i) >= 30:
        id = i
print(id)

gdd.download_file_from_google_drive(file_id = id, dest_path = './question.zip', unzip = True)

path = os.getcwd()
os.remove(str(path) + "/question.zip")