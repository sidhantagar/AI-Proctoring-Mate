#IMPORT HERE..
import os

def remove_file(file_name, file_path = None):
    if file_path != None:
        file_name += file_path
    if os.path.exists(file_name):
        os.remove(file_name)