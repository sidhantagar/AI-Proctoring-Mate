#IMPORT HERE..
from selenium import webdriver
import os
import File_Remover

#DEFINE CONSTANTS HERE..
TEST_CODE = None
FILE_NAME = None
PATH = None
URL = None

def upload_file():
    driver = webdriver.Chrome(executable_path= PATH +"\\chromedriver_win32\\chromedriver.exe")
    driver.implicitly_wait(20)
    if __name__ != "__main__":
        driver.minimize_window()
    driver.get(URL)
    uploader = driver.find_element_by_id("customFile")
    uploader.send_keys(PATH + "\\"+FILE_NAME)
    driver.find_element_by_id("submitButton").click()
    driver.close()
    driver.quit()

def define_constants(file_name, test_code):
    global TEST_CODE, FILE_NAME, PATH, URL
    FILE_NAME = file_name
    TEST_CODE = test_code
    PATH = os.path.dirname(os.path.abspath(__file__))
    URL = "http://localhost:8000/questions/submitAnswers/"

def upload_submission(fileName, testCode):
    define_constants(fileName, testCode)
    upload_file()
    File_Remover.remove_file(fileName)
    

if __name__=='__main__':
    upload_submission(fileName = "3uibkub_Sidhant-Agarwal_20188028_responses.csv", testCode = "3uibkub")