import random
import array
import uuid
import datetime
import pandas as pd
from urllib.request import urlopen

# Utility functions for Questions App.

# generate a testCode
def generateTestCode(length):

    if length > 12:
        return None

    MAX_LEN = length

    digits = '123456789'
    digits = list(digits)

    upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    upper_case = list(upper_case)

    combined_list = digits + upper_case

    temp_pass = random.choice(digits) + random.choice(upper_case)
    temp_pass_list = []

    for i in range(MAX_LEN-2):

        temp_pass = temp_pass + random.choice(combined_list)

        temp_pass_list = array.array('u',temp_pass)
        random.shuffle(temp_pass_list)

    code = ""
    for i in temp_pass_list:
        code = code + i

    return code

# scamble the testCode
def scrammbleCode(code):

    newCode = ""
    for ch in code:

        if ord(ch)>=65 and ord(ch)<=90:
            newCode = newCode + chr(ord(ch)+32)
        else:
            newCode = newCode + chr(ord(ch)-1)

    return newCode

# unscramble the scrambled testCode
def unscrambleCode(code):

    orgCode = ""
    for ch in code:

        if(ord(ch)>=97 and ord(ch)<=122):
            orgCode = orgCode + chr(ord(ch)-32)
        else:
            orgCode = orgCode + chr(ord(ch)+1)

    return orgCode

# for creating the slug and hiding test link in it.
def hideCode(code):

    slug = str(uuid.uuid4())

    slug = slug + '-' + code
    return slug

# Extract the code from slug.
def extractCode(slug):

    code = ""
    if slug is not None:
        slug_list = slug.split('-')
        code = code + slug_list[-1]

    else:
        return None

    return code


# use for addQuestions form purposes.
def scramble(code):

    str = ""
    for i in range(len(code)):
        temp = ""
        if(ord(code[i])>=65 and ord(code[i])<=90):
            temp = temp + chr(ord(code[i])+32)
        else:
            temp = code[i]

        if(i%2):
            str = temp + str
        else:
            str = str + temp

    return str

def descramble(code):

    str = ""
    i = len(code)//2
    j = i-1
    while(i<=len(code)-1 and j>=0):

        if(ord(code[i])>=97 and ord(code[i])<=122):
            str = str + chr(ord(code[i])-32)
        else:
            str = str + code[i]

        if(ord(code[j])>=97 and ord(code[j])<=122):
            str = str + chr(ord(code[j])-32)
        else:
            str = str + code[j]

        i += 1
        j -= 1

    return str

def get_server_time():
    get_time = urlopen('http://just-the-time.appspot.com/')
    get_time = get_time.read().strip().decode('utf-8')
    date = [int (x) for x in (get_time.split(' ')[0]).split('-')]
    time = [int (x) for x in (get_time.split(' ')[1]).split(':')]
    datetime_today = datetime.datetime(date[0], date[1], date[2], time[0], time[1]) + datetime.timedelta(minutes= 325)
    return datetime_today

def get_end_time(date,time,duration):

    date = [int(x) for x in date.split('-')]
    time = [int(x) for x in time.split(":")]
    duration_ = int(duration)
    datetime_scheduled = datetime.datetime(date[0], date[1], date[2], time[0], time[1]) + datetime.timedelta(minutes= duration_)
    return datetime_scheduled

def check_datetime(date,time,duration):

    now = get_server_time()
    end = get_end_time(date,time,duration)

    # print(end,now,(end-now).total_seconds())

    if ((end-now).total_seconds()) >= 0:
        return 1
    else:
        return 0
