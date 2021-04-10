#Local python path C:\Users\Sidhant Agarwal\AppData\Local\Programs\Python\Python36
#Note : Due to compatibility issues with pyaudio, This module will not work on python 3.5 or higher

#IMPORT HERE..
import cv2
import numpy as np
import pyaudio
import wave
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import pandas as pd
import AV_Synchronization
import UI_Comp_Functions

NAME = None
UNIQUE_ID = None
Q_WIDTH = None
N_WIDTH = None
HEIGHT = None
PADX = None
PADY = None
ROOT = None
SUSPICIOUS_THRESHOLD = None
STATUS_FONT = None
BUTTON_FONT = None
CONTRAST_COLOURS = None
DICTIONARY_COLOURS = None
CALCULATOR_ICON = None
DF_CONFIGURATION = None
DURATION = None

av_index = None
recording = None
cap = None
aud = None
vid_frame_width = None
vid_frame_height = None
option_variable = None
video_app_frame = None
question_frame = None
options_frame = None
navigation_frame_1 = None
df_responses = None
calculator = None
lmain = None
status = None
calculator_status = None
time_lapsed = None
timer_label = None

def define_constants(name, unique_id):
    global Q_WIDTH, N_WIDTH, HEIGHT, PADX, PADY, ROOT, SUSPICIOUS_THRESHOLD, STATUS_FONT, BUTTON_FONT, CONTRAST_COLOURS, DICTIONARY_COLOURS, CALCULATOR_ICON, NAME, UNIQUE_ID, DF_CONFIGURATION, DURATION
    NAME = name
    UNIQUE_ID = unique_id
    Q_WIDTH = 8
    N_WIDTH = 11
    HEIGHT = 2
    PADX = 3
    PADY = 2
    ROOT = tk.Tk()
    ROOT.minsize(1400,800)
    ROOT.protocol("WM_DELETE_WINDOW", window_close)
    SUSPICIOUS_THRESHOLD = 0.5
    STATUS_FONT = tkfont.Font(family = "Comic Sans MS", size = 15)
    BUTTON_FONT = tkfont.Font(family = "Comic Sans MS", size = 13)
    CONTRAST_COLOURS = {-1 : 'white', 0 : 'white', 1 : 'black', 2 : 'black', 3 : 'black', 4 : 'black'}
    DICTIONARY_COLOURS = {-1 : 'purple', 0 : 'red', 1 : 'green', 2 : 'green', 3 : 'green', 4 : 'green'}
    CALCULATOR_ICON = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv2.resize(cv2.imread(r'UI_Images\calculator.jpg'), (0, 0), fx = 0.3, fy = 0.3), cv2.COLOR_BGR2RGBA)))
    DF_CONFIGURATION = pd.read_csv('./Question/Config.csv').set_index("Name")[['Value']]
    DURATION = (int(DF_CONFIGURATION.at['Duration', 'Value']))*60

def define_initializations():
    global av_index, recording, cap, aud, vid_frame_width, vid_frame_height, option_variable, video_app_frame, question_frame, options_frame, navigation_frame_1, df_responses, calculator, calculator_status, time_lapsed
    av_index = 1
    recording = 0 

    cap = cv2.VideoCapture(0)
    aud = pyaudio.PyAudio()
    vid_frame_width = int(cap.get(3))
    vid_frame_height = int(cap.get(4))
    video_app_frame = tk.Frame(ROOT)
    video_app_frame.place (x = 1070, y = 60)
    question_frame = tk.Frame(ROOT)
    question_frame.place(x = 15, y = 10)
    options_frame = tk.Frame(ROOT)
    options_frame.place(x = 15, y = 130)
    navigation_frame_1 = tk.Frame(ROOT)
    navigation_frame_1.place(x = 1070, y = 350)
    option_variable = tk.IntVar()
    df_responses = pd.DataFrame([[0,-1], [1, -1], [2, -1], [3, -1], [4, -1], [5, -1], [6, -1], [7, -1], [8, -1], [9, -1], [10, -1], [11, -1], [12, -1]],columns = ['Question', 'Response'])
    df_responses.set_index('Question')

    calculator = tk.Button(ROOT, text = "", image = CALCULATOR_ICON, relief = 'raised', bd = 4, command = calc_function, state = DF_CONFIGURATION.at['Calculator','Value'] )
    calculator.place(x = 1347, y = 1)
    calculator_status = "closed"
    time_lapsed = 14*60+40

def reset_config():
    global calculator_status
    if calculator_status == "open":
        calculator_status = "closed"
        reset_navigation_frame()
    b1 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.1', command = button_1, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][1]], fg = CONTRAST_COLOURS[df_responses['Response'][1]], font = BUTTON_FONT)
    b1.grid(column = 1, row = 1, padx = PADX, pady = PADY)
    b2 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.2', command = button_2, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][2]], fg = CONTRAST_COLOURS[df_responses['Response'][2]], font = BUTTON_FONT)
    b2.grid(column = 2, row = 1, padx = PADX, pady = PADY)
    b3 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.3', command = button_3, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][3]], fg = CONTRAST_COLOURS[df_responses['Response'][3]], font = BUTTON_FONT)
    b3.grid(column = 3, row = 1, padx = PADX, pady = PADY)
    b4 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.4', command = button_4, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][4]], fg = CONTRAST_COLOURS[df_responses['Response'][4]], font = BUTTON_FONT)
    b4.grid(column = 1, row = 2, padx = PADX, pady = PADY)
    b5 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.5', command = button_5, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][5]], fg = CONTRAST_COLOURS[df_responses['Response'][5]], font = BUTTON_FONT)
    b5.grid(column = 2, row = 2, padx = PADX, pady = PADY)
    b6 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.6', command = button_6, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][6]], fg = CONTRAST_COLOURS[df_responses['Response'][6]], font = BUTTON_FONT)
    b6.grid(column = 3, row = 2, padx = PADX, pady = PADY)
    b7 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.7', command = button_7, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][7]], fg = CONTRAST_COLOURS[df_responses['Response'][7]], font = BUTTON_FONT)
    b7.grid(column = 1, row = 3, padx = PADX, pady = PADY)
    b8 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.8', command = button_8, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][8]], fg = CONTRAST_COLOURS[df_responses['Response'][8]], font = BUTTON_FONT)
    b8.grid(column = 2, row = 3, padx = PADX, pady = PADY)
    b9 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.9', command = button_9, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][9]], fg = CONTRAST_COLOURS[df_responses['Response'][9]], font = BUTTON_FONT)
    b9.grid(column = 3, row = 3, padx = PADX, pady = PADY)
    b10 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.10', command = button_10, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][10]], fg = CONTRAST_COLOURS[df_responses['Response'][10]], font = BUTTON_FONT)
    b10.grid(column = 1, row = 4, padx = PADX, pady = PADY)
    b11 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.11', command = button_11, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][11]], fg = CONTRAST_COLOURS[df_responses['Response'][11]], font = BUTTON_FONT)
    b11.grid(column = 2, row = 4, padx = PADX, pady = PADY)
    b12 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.12', command = button_12, relief = 'raised', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][12]], fg = CONTRAST_COLOURS[df_responses['Response'][12]], font = BUTTON_FONT)
    b12.grid(column = 3, row = 4, padx = PADX, pady = PADY)

def submit_test():
    window_close()

def reset_navigation_frame():
    global navigation_frame_1
    navigation_frame_1.destroy()
    navigation_frame_1 = tk.Frame(ROOT)
    navigation_frame_1.place(x = 1070, y = 350)

def calc_function():
    global calculator_status
    if calculator_status == "closed":
        calculator_status = "open"
        reset_navigation_frame()
        UI_Comp_Functions.display_calculator(navigation_frame_1)
    elif calculator_status == "open":
        reset_config()

def button_1():
    def clear_response():
        df_responses['Response'][1] = 0
        button_1()
    if (df_responses['Response'][1] == -1):
        df_responses['Response'][1] = 0
    reset_config()
    b1 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.1', command = button_1, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][1]], fg = CONTRAST_COLOURS[df_responses['Response'][1]], font = BUTTON_FONT)
    b1.grid(column = 1, row = 1, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_1, relief = 'raised', bd = 4, font = STATUS_FONT, state = 'disabled')
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_2, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_1(question_frame, options_frame, option_variable, df_responses)
def button_2():
    def clear_response():
        df_responses['Response'][2] = 0
        button_2()
    if (df_responses['Response'][2] == -1):
        df_responses['Response'][2] = 0
    reset_config()
    b2 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.2', command = button_2, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][2]], fg = CONTRAST_COLOURS[df_responses['Response'][2]], font = BUTTON_FONT)
    b2.grid(column = 2, row = 1, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_1, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_3, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_2(question_frame, options_frame, option_variable, df_responses)
def button_3():
    def clear_response():
        df_responses['Response'][3] = 0
        button_3()
    if (df_responses['Response'][3] == -1):
        df_responses['Response'][3] = 0
    reset_config()
    b3 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.3', command = button_3, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][3]], fg = CONTRAST_COLOURS[df_responses['Response'][3]], font = BUTTON_FONT)
    b3.grid(column = 3, row = 1, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_2, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_4, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_3(question_frame, options_frame, option_variable, df_responses)
def button_4():
    def clear_response():
        df_responses['Response'][4] = 0
        button_4()
    if (df_responses['Response'][4] == -1):
        df_responses['Response'][4] = 0
    reset_config()
    b4 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.4', command = button_4, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][4]], fg = CONTRAST_COLOURS[df_responses['Response'][4]], font = BUTTON_FONT)
    b4.grid(column = 1, row = 2, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_3, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_5, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_4(question_frame, options_frame, option_variable, df_responses)
def button_5():
    def clear_response():
        df_responses['Response'][5] = 0
        button_5()
    if (df_responses['Response'][5] == -1):
        df_responses['Response'][5] = 0
    reset_config()
    b5 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.5', command = button_5, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][5]], fg = CONTRAST_COLOURS[df_responses['Response'][5]], font = BUTTON_FONT)
    b5.grid(column = 2, row = 2, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_4, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_6, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_5(question_frame, options_frame, option_variable, df_responses)
def button_6():
    def clear_response():
        df_responses['Response'][6] = 0
        button_6()
    if (df_responses['Response'][6] == -1):
        df_responses['Response'][6] = 0 
    reset_config()
    b6 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.6', command = button_6, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][6]], fg = CONTRAST_COLOURS[df_responses['Response'][6]], font = BUTTON_FONT)
    b6.grid(column = 3, row = 2, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_5, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_7, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_6(question_frame, options_frame, option_variable, df_responses)
def button_7():
    def clear_response():
        df_responses['Response'][7] = 0
        button_7()
    if (df_responses['Response'][7] == -1):
        df_responses['Response'][7] = 0
    reset_config()
    b7 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.7', command = button_7, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][7]], fg = CONTRAST_COLOURS[df_responses['Response'][7]], font = BUTTON_FONT)
    b7.grid(column = 1, row = 3, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_6, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_8, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_7(question_frame, options_frame, option_variable, df_responses)
def button_8():
    def clear_response():
        df_responses['Response'][8] = 0
        button_8()
    if (df_responses['Response'][8] == -1):
        df_responses['Response'][8] = 0
    reset_config()
    b8 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.8', command = button_8, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][8]], fg = CONTRAST_COLOURS[df_responses['Response'][8]], font = BUTTON_FONT)
    b8.grid(column = 2, row = 3, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_7, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_9, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_8(question_frame, options_frame, option_variable, df_responses)
def button_9():
    def clear_response():
        df_responses['Response'][9] = 0
        button_9()
    if (df_responses['Response'][9] == -1):
        df_responses['Response'][9] = 0
    reset_config()
    b9 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.9', command = button_9, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][9]], fg = CONTRAST_COLOURS[df_responses['Response'][9]], font = BUTTON_FONT)
    b9.grid(column = 3, row = 3, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_8, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_10, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_9(question_frame, options_frame, option_variable, df_responses)
def button_10():
    def clear_response():
        df_responses['Response'][10] = 0
        button_10()
    if (df_responses['Response'][10] == -1):
        df_responses['Response'][10] = 0
    reset_config()
    b10 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.10', command = button_10, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][10]], fg = CONTRAST_COLOURS[df_responses['Response'][10]], font = BUTTON_FONT)
    b10.grid(column = 1, row = 4, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_9, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_11, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_10(question_frame, options_frame, option_variable, df_responses)
def button_11():
    def clear_response():
        df_responses['Response'][1] = 0
        button_11()
    if (df_responses['Response'][11] == -1):
        df_responses['Response'][11] = 0
    reset_config()
    b11 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.11', command = button_11, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][11]], fg = CONTRAST_COLOURS[df_responses['Response'][11]], font = BUTTON_FONT)
    b11.grid(column = 2, row = 4, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_10, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = button_12, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_11(question_frame, options_frame, option_variable, df_responses)
def button_12():
    def clear_response():
        df_responses['Response'][12] = 0
        button_12()
    if (df_responses['Response'][12] == -1):
        df_responses['Response'][12] = 0
    reset_config()
    b12 = tk.Button(navigation_frame_1, padx = PADX, pady = PADY, width = Q_WIDTH, height = HEIGHT, text = 'Q.12', command = button_12, relief = 'sunken', bd = 4, bg = DICTIONARY_COLOURS[df_responses['Response'][12]], fg = CONTRAST_COLOURS[df_responses['Response'][12]], font = BUTTON_FONT)
    b12.grid(column = 3, row = 4, padx = PADX, pady = PADY)
    previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = button_11, relief = 'raised', bd = 4, font = STATUS_FONT)
    previous_button.place(x = 15, y = 700)
    next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Submit Test', command = submit_test, relief = 'raised', bd = 4, font = STATUS_FONT)
    next_button.place(x = 900, y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH+5, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x =457, y = 700)
    UI_Comp_Functions.button_12(question_frame, options_frame, option_variable, df_responses)

def dynamic_initialization():
    global lmain,status
    lmain = tk.Label(video_app_frame, anchor = 'ne')
    lmain.grid(row = 1, column = 1)
    status = tk.Label(video_app_frame, text = 'The status will show here!', font = STATUS_FONT, width = 27)
    status.grid(row = 2, column = 1)


def record_if_suspicious(vid_frame):
    global av_index
    global recording
    global SUSPICIOUS_THRESHOLD
    #get suspicious value here
    suspicious_value = 0.7
    #...
    if suspicious_value >= SUSPICIOUS_THRESHOLD:
        if recording == 0:
            AV_Synchronization.start_AVrecording(filename = 'video_'+ str(av_index), video_capture = cap)
            recording = 1
    else:
        if recording == 1:
            AV_Synchronization.stop_AVrecording(filename = 'video_'+ str(av_index))
            AV_Synchronization.file_manager()
            av_index+=1
            recording = 0

def base_function():
    ret, vid_frame = cap.read()
    record_if_suspicious(vid_frame)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv2.resize(vid_frame, (0, 0), fx = 0.5, fy = 0.5) , cv2.COLOR_BGR2RGBA)))
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, base_function)   

def show_timer():
    global time_lapsed, timer_label
    if time_lapsed == DURATION:
        submit_test()
        return
    if __name__ == '__main__':
        print(time_lapsed)
    time_lapsed = time_lapsed + 1
    if time_lapsed >= 0.8*DURATION:
        color = "red"
    else:
        color = "black"
    timer_label = tk.Label(ROOT, text = "Time Remaining: "+str((DURATION-time_lapsed)//60)+":"+ str((DURATION-time_lapsed)%60), fg = color, width = 18 , font = STATUS_FONT)
    timer_label.place(x = 1060, y = 10)
    timer_label.after(1000, show_timer)

def window_close():
    if recording == 1:
        AV_Synchronization.stop_AVrecording(filename = 'video_'+ str(av_index))
        AV_Synchronization.file_manager()
    cap.release()
    df_responses[1:].to_csv(NAME + "_"+ UNIQUE_ID +"_responses.csv", index = False)
    ROOT.destroy()

def main(name = 'Sidhant Agarwal', unique_id = "20188028"):
    define_constants(name, unique_id)
    define_initializations()
    dynamic_initialization()
    UI_Comp_Functions.initialize_ui_components()
    reset_config()
    button_1()
    show_timer()
    base_function() #Commented temporarily................................
    ROOT.mainloop()

if __name__ == "__main__":
    main()