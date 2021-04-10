#IMPORT HERE..
import os
import time
from zipfile import ZipFile 
from selenium import webdriver

#DEFINE CONSTANTS HERE..
URL = 'http://localhost:8000/CollectMaterial/'
PATH = os.getcwd()

def fetch_questions(code):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : PATH+"\Question"}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path= PATH +"\\chromedriver_win32\\chromedriver.exe", chrome_options= chrome_options)
    driver.implicitly_wait(20)
    driver.get(URL)
    if __name__ != "__main__":
        driver.minimize_window()
    uploader = driver.find_element_by_id("test_code")
    uploader.send_keys(code)
    driver.find_element_by_id("submit").click()
    time.sleep(2)
    status = driver.current_url[-4:]
    driver.close()
    driver.quit()

    if  status == "True":
        return False
    else:
        os.mkdir(PATH+"\\Question\\"+ code)
        with ZipFile(PATH+"\Question\Question.zip","r") as zip_ref:
            zip_ref.extractall(PATH+"\\Question\\"+ code)
        os.remove(PATH+"\Question\Question.zip")
        return True    


if __name__ == '__main__':
    print(PATH)
    print(fetch_questions(code = 'FF5G9Z22'))