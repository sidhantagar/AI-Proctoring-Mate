from selenium import webdriver
import os
import unittest
import HtmlTestRunner


TEST_CODE = None
FILE_NAME = None
PATH = None

def upload_file():
    driver = webdriver.Chrome(executable_path=r".\chromedriver_win32\chromedriver.exe")
    driver.implicitly_wait(20)
    driver.minimize_window()
    driver.get("http://localhost:8000/questions/submitAnswers/")
    uploader = driver.find_element_by_id("customFile")
    uploader.send_keys(PATH + "\\"+FILE_NAME)
    driver.find_element_by_id("submitButton").click()
    driver.close()
    driver.quit()



def define_constants(file_name, test_code):
    global TEST_CODE, FILE_NAME, PATH
    FILE_NAME = file_name
    TEST_CODE = test_code
    PATH = os.path.dirname(os.path.abspath(__file__))



def upload_submission(file_name = "Sidhant Agarwal_20188028_responses.csv", test_code = "3uibkub"):
    define_constants(file_name, test_code)
    upload_file()


if __name__=='__main__':
    upload_submission()