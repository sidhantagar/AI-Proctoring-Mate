#IMPORT HERE..
import os
import requests
from google_drive_downloader import GoogleDriveDownloader as gdd

#DEFINE CONSTANTS HERE..
SHORTNER = 'http://bit.ly/'
PATH = os.getcwd()

def remove_redundant_files():
    try:
        os.remove(str(PATH)+"/Question/Config.csv")
    except:
        pass
    finally:
        pass    
    try:
        os.remove(str(PATH)+"/Question/Questions.csv")
    except:
        pass
    finally:
        pass

def fetch_questions(code = '3uibkub'):
    remove_redundant_files()    #Removes old data files
    r = requests.get(SHORTNER+code)
    url = r.url
    if __name__ == '__main__':
        print(url)
    for i in url.split('/'):
        if len(i) >= 30:
            id = i
    if __name__ == '__main__':
        print(id)

    gdd.download_file_from_google_drive(file_id = id, dest_path = './question.zip', unzip = True)
    os.remove(str(PATH) + "/question.zip")

if __name__ == '__main__':
    fetch_questions()