#IMPORT HERE..
from selenium import webdriver
import os
import time
import pandas as pd

#DEFINE CONSTANTS HERE..
TEST_CODE = None
PATH = None
URL = None

def upload_file():
    driver = webdriver.Chrome(executable_path= PATH +"\\chromedriver_win32\\chromedriver.exe")
    driver.implicitly_wait(20)
    if __name__ != "__main__":
        pass
        #driver.minimize_window()
    driver.get(URL)
    uploader = driver.find_element_by_id("response_file")
    uploader.send_keys(PATH + "\\"+FILE_NAME)
    if __name__ != "__main__":
        time.sleep(2)
    driver.find_element_by_id("submitButton").click()
    if __name__ != "__main__":
        time.sleep(2)
    driver.close()
    driver.quit()

def define_constants(file_name):
    global FILE_NAME, PATH, URL
    FILE_NAME = file_name
    PATH = os.path.dirname(os.path.abspath(__file__))
    URL = "http://localhost:8000/questions/submitAnswers/"

def upload_submission(fileName):
    define_constants(fileName)
    upload_file()
    

if __name__=='__main__':
    DF_CONFIGURATION = pd.read_csv("./Question/" + "3uibkub" + "/Config.csv").set_index("Name")[['Value']]
    upload_submission(fileName = "3uibkub_Sidhant-Agarwal_20188028_responses.csv", testCode = "3uibkub", config = DF_CONFIGURATION)