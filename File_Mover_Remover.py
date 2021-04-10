#IMPORT HERE..
import os
import shutil

def remove_file(file_name, file_path = None):
    if file_path != None:
        file_name += file_path
    if os.path.exists(file_name):
        os.remove(file_name)

def move_answer(file_name, test_code):
    os.mkdir(".\\Answer\\"+test_code)
    shutil.copy(".\\"+file_name, ".\\Answer\\"+test_code)
    os.remove(".\\"+file_name)

def remove_test_files(code):
    shutil.rmtree(".\\Question\\"+code)