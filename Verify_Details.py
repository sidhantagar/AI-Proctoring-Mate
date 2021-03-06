#IMPORT HERE..
import pandas as pd

#DEFINE CONSTANTS HERE..
DF_CONFIGURATION = None
ID_FORMAT = None

def define_constants(CODE):
    global DF_CONFIGURATION, ID_FORMAT
    DF_CONFIGURATION = pd.read_csv("./Question/" + CODE + "/Config.csv").set_index("Name")[['Value']]
    ID_FORMAT = DF_CONFIGURATION.at['Id_format','Value']

def verify_details(unique_id, CODE):
    define_constants(CODE)
    if __name__ == '__main__':
        print(ID_FORMAT)
    if len(unique_id) != len(ID_FORMAT):
        return False
    for i,j in zip(ID_FORMAT, unique_id):
        if i == 'a' or i == 'A':
            if j.isalpha() != True:
                return False
        elif i == 'n' or i == 'N':
            if j.isnumeric() != True:
                return False
        elif i == 'c' or i == 'C':
            pass
        else:
            if i != j:
                return False
    return True
            
if __name__ == '__main__':
    print(verify_details('a120188028'))
