import pandas as pd

DF_CONFIGURATION = None
ID_FORMAT = None

def define_constants():
    global DF_CONFIGURATION, ID_FORMAT
    DF_CONFIGURATION = pd.read_csv('./Question/Config.csv').set_index("Name")[['Value']]
    ID_FORMAT = DF_CONFIGURATION.at['Id_format','Value']

def verify_details(unique_id):
    define_constants()
    if __name__ == '__main__':
        print(ID_FORMAT)
    if len(unique_id) != len(ID_FORMAT):
        return False
    for i,j in zip(ID_FORMAT, unique_id):
        if i == 'a':
            if j.isalpha() != True:
                return False
        elif i == 'n':
            if j.isnumeric() != True:
                return False
        elif i == 'c':
            pass
        else:
            if i != j:
                return False
    return True
            
if __name__ == '__main__':
    print(verify_details('a120188028'))
