import datetime
import pandas as pd
from urllib.request import urlopen

DF_CONFIGURATION = None

def define_constants(code):
    global DF_CONFIGURATION
    DF_CONFIGURATION = pd.read_csv("./Question/" + code + "/Config.csv").set_index("Name")[['Value']]

def get_server_time():
    get_time = urlopen('http://just-the-time.appspot.com/')
    get_time = get_time.read().strip().decode('utf-8')
    date = [int (x) for x in (get_time.split(' ')[0]).split('-')]
    time = [int (x) for x in (get_time.split(' ')[1]).split(':')]
    datetime_today = datetime.datetime(date[0], date[1], date[2], time[0], time[1]) + datetime.timedelta(minutes= 330)
    return datetime_today

def get_end_time():
    date = [int (x) for x in DF_CONFIGURATION.at["Scheduled_Date", "Value"].split('-')]
    time = [int (x) for x in DF_CONFIGURATION.at["Scheduled_Time", "Value"].split(":")]
    duration = int(DF_CONFIGURATION.at["Duration", "Value"])
    datetime_scheduled = datetime.datetime(date[0], date[1], date[2], time[0], time[1]) + datetime.timedelta(minutes= duration)
    return datetime_scheduled

def check_datetime(code):
    define_constants(code)

    now = get_server_time()
    end = get_end_time()
    
    if ((end-now).total_seconds())//60 > int(DF_CONFIGURATION.at["Duration", "Value"]) :
        return 2   
    elif ((end-now).total_seconds())//60 >= 5:
        return 3
    elif ((end-now).total_seconds())//60 >= 0:
        return 1 #Not enough time
    else:
        return 0

def time_until_end(code): #In seconds
    define_constants(code)

    now = get_server_time()
    end = get_end_time()
    
    return (end - now).total_seconds()

def time_until_start(code): #In minutes
    define_constants(code)

    now = get_server_time()
    end = get_end_time()

    return ((end-now).total_seconds())//60 - int(DF_CONFIGURATION.at["Duration", "Value"])


if __name__ == '__main__':
    print(check_datetime("16KEEF59"))
