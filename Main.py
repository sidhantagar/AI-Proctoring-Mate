#Local python path C:\Users\Sidhant Agarwal\AppData\Local\Programs\Python\Python36
#Note : Due to compatibility issues with pyaudio, This module will not work on python 3.5 or higher

#IMPORT HERE..
import cv2
import pyaudio
import shuffler
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import AV_Synchronization
import UI_Comp_Functions
import Upload_Submission
from functools import partial
import Render_Button
import Check_Datetime

#DEFINE CONSTANTS HERE..
CODE = None
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
NUM_QUESTIONS = None
NUM_SECTIONS = None
NAME_TO_RGB = None

#INITIALISE GLOBAL VARIABLES HERE..
button_icons = None
av_index = None
recording = None
cap = None
aud = None
vid_frame_width = None
vid_frame_height = None
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
button_img = None
buttons = None
active_section = None
warning_1 = None
warning_time = None
warning_label = None

def define_constants(name, unique_id, code):
    global Q_WIDTH, N_WIDTH, HEIGHT, PADX, PADY, ROOT, SUSPICIOUS_THRESHOLD, STATUS_FONT, BUTTON_FONT, CONTRAST_COLOURS, DICTIONARY_COLOURS, CALCULATOR_ICON, NAME, UNIQUE_ID, DF_CONFIGURATION, DURATION, CODE, NUM_QUESTIONS, NUM_SECTIONS, NAME_TO_RGB
    CODE = code
    NAME = "-".join(name.split(" "))
    UNIQUE_ID = unique_id
    Q_WIDTH = 8
    N_WIDTH = 11
    HEIGHT = 2
    PADX = 3
    PADY = 2
    ROOT = tk.Tk()
    ROOT.minsize(1400,800)
    ROOT['bg'] = "gray13"      #Termorarily changed to black theme :P 
    ROOT.protocol("WM_DELETE_WINDOW", window_close)
    SUSPICIOUS_THRESHOLD = 0.5
    STATUS_FONT = tkfont.Font(family = "Comic Sans MS", size = 15)
    BUTTON_FONT = tkfont.Font(family = "Comic Sans MS", size = 13)
    CONTRAST_COLOURS = {-1 : 'white', 0 : 'white'}
    DICTIONARY_COLOURS = {-1 : 'purple', 0 : 'red'}
    for i in range(1,16):
        CONTRAST_COLOURS[i] = 'white'
        DICTIONARY_COLOURS[i] = 'green'
    CALCULATOR_ICON = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv2.resize(cv2.imread(r'UI_Images\calculator.jpg'), (0, 0), fx = 0.3, fy = 0.3), cv2.COLOR_BGR2RGBA)))
    DF_CONFIGURATION = pd.read_csv("./Question/" + CODE + "/Config.csv").set_index("Name")[['Value']]
    if CODE == "PRACTICE":
        DURATION = 10*60
    else:
        DURATION = (int(DF_CONFIGURATION.at['Duration', 'Value']))*60 + 90 #Correction for instruction_menu
    NUM_SECTIONS = (int(DF_CONFIGURATION.at['Num_sections', 'Value']))
    NUM_QUESTIONS = []
    for i in range(1, NUM_SECTIONS+1):
        NUM_QUESTIONS.append(int(DF_CONFIGURATION.at['Num_questions_'+str(i), 'Value']))
        assert NUM_QUESTIONS[i-1]>1 #Needed to mantain the structure in next and previous navigation buttons
    NAME_TO_RGB = {"purple" : (128, 0, 128), "white" : (255, 255, 255), "green" : (0, 128, 0), "red" : (255, 0 , 0), "black" : (0, 0, 0)}

def define_initializations():
    global av_index, recording, cap, aud, vid_frame_width, vid_frame_height, video_app_frame, question_frame, options_frame, navigation_frame_1, df_responses, calculator, calculator_status, time_lapsed, warning_1
    av_index = 1
    recording = 0 
    cap = cv2.VideoCapture(0)
    aud = pyaudio.PyAudio()
    vid_frame_width = int(cap.get(3))
    vid_frame_height = int(cap.get(4))
    video_app_frame = tk.Frame(ROOT)
    video_app_frame.place (x = 1070, y = 60)
    question_frame = tk.Frame(ROOT)
    question_frame.place(x = 15, y = 110)
    options_frame = tk.Frame(ROOT)
    options_frame.place(x = 15, y = 230)
    navigation_frame_1 = tk.Frame(ROOT)
    navigation_frame_1.place(x = 1070, y = 350)
    df_responses = pd.DataFrame()
    for i in range(1, (NUM_SECTIONS+1)):
        df_responses["Response_section_" + str(i)] = [-1]*(max(NUM_QUESTIONS)+1)
        df_responses["Marked_section_" + str(i)] = [False]*(max(NUM_QUESTIONS)+1)
    calculator = tk.Button(ROOT, text = "", image = CALCULATOR_ICON, relief = 'raised', bd = 4, command = calc_function, state = DF_CONFIGURATION.at['Calculator','Value'] )
    calculator.place(x = 1347, y = 1)
    calculator_status = "closed"
    if CODE == "PRACTICE":
        time_lapsed = 0
    else:
        time_lapsed = DURATION - Check_Datetime.time_until_end(CODE)
    warning_1 = 2

def reset_section_config():
    section_1 = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Section 1', command = lambda : load_section(1), relief = 'raised', bd = 4, font = STATUS_FONT)
    section_1.place(x = 15, y = 15)
    section_2 = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Section 2', command = lambda : load_section(2), relief = 'raised', bd = 4, font = STATUS_FONT, state = {1 : "disabled", 2 : "normal", 3 : "normal"}[NUM_SECTIONS])
    section_2.place(x = 460, y = 15)
    section_3 = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Section 3', command = lambda : load_section(3), relief = 'raised', bd = 4, font = STATUS_FONT, state = {1 : "disabled", 2 : "disabled", 3 : "normal"}[NUM_SECTIONS])
    section_3.place(x = 875, y = 15)

def load_section(num_section):
    reset_navigation_frame()
    reset_section_config()
    if num_section == 1:
        section_1 = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Section 1', command = lambda : load_section(1), relief = 'sunken', bd = 4, font = STATUS_FONT)
        section_1.place(x = 15, y = 15)
    if num_section == 2:
        section_2 = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Section 2', command = lambda : load_section(2), relief = 'sunken', bd = 4, font = STATUS_FONT, state = {1 : "disabled", 2 : "normal", 3 : "normal"}[NUM_SECTIONS])
        section_2.place(x = 460, y = 15)
    if num_section == 3:
        section_3 = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Section 3', command = lambda : load_section(3), relief = 'sunken', bd = 4, font = STATUS_FONT, state = {1 : "disabled", 2 : "disabled", 3 : "normal"}[NUM_SECTIONS])
        section_3.place(x = 875, y = 15)
    global active_section
    active_section = num_section
    UI_Comp_Functions.select_question_set(num_section)
    button_num(1)

def reset_config():
    global calculator_status, button_icons
    if calculator_status == "open":
        calculator_status = "closed"
        reset_navigation_frame()
    button_icons = []
    for i in range(1, NUM_QUESTIONS[active_section-1]+1):
        active_question = shuffler.shuffle_question_num(i,active_section)
        button_icons.append(ImageTk.PhotoImage(image=Image.fromarray(Render_Button.render_button(question_num = i, marked_for_review = df_responses['Marked_section_' + str(active_section)][active_question], bg_color = NAME_TO_RGB[DICTIONARY_COLOURS[df_responses['Response_section_' + str(active_section)][active_question]]], font_color = NAME_TO_RGB[CONTRAST_COLOURS[df_responses['Response_section_' + str(active_section)][active_question]]]))))
        button = tk.Button(navigation_frame_1, text = "", image = button_icons[i-1], relief = 'raised', bd = 4, command = partial(button_num, i), bg = DICTIONARY_COLOURS[df_responses['Response_section_' + str(active_section)][active_question]])
        button.grid(column = ((i-1)%3)+1, row = (i + 2)//3, padx = PADX, pady = PADY)

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

def button_num(question_num):
    global button_img
    active_question = shuffler.shuffle_question_num(question_num, active_section)
    def clear_response():
        df_responses['Response_section_' + str(active_section)][active_question] = 0
        button_num(question_num)
    def mark_question():
        df_responses['Marked_section_' + str(active_section)][active_question] = True
        button_num(question_num)
    def unmark_question():
        df_responses['Marked_section_' + str(active_section)][active_question] = False
        button_num(question_num)
    if (df_responses['Response_section_' + str(active_section)][active_question] == -1):
        df_responses['Response_section_' + str(active_section)][active_question] = 0
    reset_config()
    button_img = ImageTk.PhotoImage(image=Image.fromarray(Render_Button.render_button(question_num = question_num, marked_for_review = df_responses['Marked_section_' + str(active_section)][active_question], bg_color = NAME_TO_RGB[DICTIONARY_COLOURS[df_responses['Response_section_' + str(active_section)][active_question]]], font_color = NAME_TO_RGB[CONTRAST_COLOURS[df_responses['Response_section_' + str(active_section)][active_question]]])))
    button = tk.Button(navigation_frame_1, text = "", image = button_img, relief = 'sunken', bd = 4, command = partial(button_num, question_num), bg = DICTIONARY_COLOURS[df_responses['Response_section_' + str(active_section)][active_question]])    
    button.grid(column = ((question_num - 1)%3)+1, row = (question_num + 2)//3, padx = PADX, pady = PADY)
    if question_num == 1:
        previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = None, relief = 'raised', bd = 4, font = STATUS_FONT, state = 'disabled')
        previous_button.place(x = 15, y = 700)
    else:
        previous_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Previous', command = partial(button_num, question_num-1), relief = 'raised', bd = 4, font = STATUS_FONT)
        previous_button.place(x = 15, y = 700)
    if question_num == NUM_QUESTIONS[active_section-1] and active_section == NUM_SECTIONS:
        next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Submit Test', command = submit_test, relief = 'raised', bd = 4, font = STATUS_FONT)
        next_button.place(x = 900, y = 700)
    elif question_num == NUM_QUESTIONS[active_section-1]:
        next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next Section', command = lambda : load_section(active_section+1), relief = 'raised', bd = 4, font = STATUS_FONT)
        next_button.place(x = 900, y = 700)
    else:
        next_button = tk.Button(ROOT, padx = PADX+3, pady = 0, width = N_WIDTH, height = HEIGHT, text = 'Next', command = partial(button_num, question_num+1), relief = 'raised', bd = 4, font = STATUS_FONT)
        next_button.place(x = 900, y = 700)
    mark_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH + 3, height = HEIGHT, text = 'Mark Question', command = mark_question, relief = 'raised', bd = 4, font = STATUS_FONT)
    mark_button.place(x = 445 , y = 700)
    unmark_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH + 3, height = HEIGHT, text = 'Unmark Question', command = unmark_question, relief = 'raised', bd = 4, font = STATUS_FONT)
    unmark_button.place(x = 670 , y = 700)
    clear_button = tk.Button(ROOT, padx = PADX, pady = 0, width = N_WIDTH + 3, height = HEIGHT, text = 'Clear Response', command = clear_response, relief = 'raised', bd = 4, font = STATUS_FONT)
    clear_button.place(x = 210, y = 700)

    UI_Comp_Functions.button_num(question_frame, options_frame, df_responses, question_num)
    if __name__ == '__main__':
        print(question_num)

def dynamic_initialization():
    global lmain,status
    shuffler.initialze_shuffler(DF_CONFIGURATION, NUM_QUESTIONS)
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
    global time_lapsed, timer_label, warning_time, warning_label,warning_1
    if time_lapsed == DURATION:
        submit_test()
        return
    if __name__ == '__main__':
        #print(time_lapsed)
        pass
    if ROOT.focus_get() == None:
        if __name__ == '__main__':
            print("Trying")
        if warning_1 == 0:
            submit_test()
            return
        if warning_1 != 2:
            warning_label = UI_Comp_Functions.display_warning(1, ROOT)
            warning_time = time_lapsed
        warning_1 -=1
    
    if warning_time != None and time_lapsed == warning_time + 8:
        warning_label.destroy()
        warning_time = None

    time_lapsed = time_lapsed + .5
    if time_lapsed >= 0.8*DURATION:
        color = "red"
        timer_label = tk.Label(ROOT, text = "Time Remaining: "+str("%0*d" % (2, ((DURATION-time_lapsed)//60)))+":"+ str("%0*d" % (2, ((DURATION-time_lapsed)%60))), fg = color, width = 18 , font = STATUS_FONT)
        if DURATION - time_lapsed < 15:
            if time_lapsed % 1 == 0:
                timer_label = tk.Label(ROOT, text = "Time Remaining: "+str("%0*d" % (2, ((DURATION-time_lapsed)//60)))+":"+ str("%0*d" % (2, ((DURATION-time_lapsed)%60))), fg = color, width = 18 , font = STATUS_FONT)    
            else:
                timer_label = tk.Label(ROOT, text = "", width = 18, font = STATUS_FONT)
    else:
        color = "black"
        timer_label = tk.Label(ROOT, text = "Time Remaining: "+str("%0*d" % (2, ((DURATION-time_lapsed)//60)))+":"+ str("%0*d" % (2, ((DURATION-time_lapsed)%60))), fg = color, width = 18 , font = STATUS_FONT)
    timer_label.place(x = 1060, y = 10)
    timer_label.after(500, show_timer)

def window_close():
    global av_index
    if recording == 1:
        AV_Synchronization.stop_AVrecording(filename = CODE + "_" + NAME + '_'+ UNIQUE_ID + "_video"+str(av_index))
        av_index += 1
        AV_Synchronization.file_manager()
    cap.release()
    file_name = CODE + "_" + NAME + "_"+ UNIQUE_ID +"_responses.csv"
    df_responses[1:].to_csv(file_name, index = False)
    ROOT.destroy()
    if CODE != 'PRACTICE': 
        Upload_Submission.upload_submission(fileName = file_name, testCode = CODE, config = DF_CONFIGURATION)#Commented temporarily................................
        for i in range(1,av_index):
            Upload_Submission.upload_submission(fileName = CODE + "_" + NAME + '_'+ UNIQUE_ID + "_video"+str(i)+".avi", testCode = "AAAAAAAA")

def main(name, unique_id, code, test_mode = True):
    define_constants(name, unique_id, code)
    define_initializations()
    dynamic_initialization()
    UI_Comp_Functions.initialize_ui_components(CODE)
    load_section(1)
    show_timer()
    base_function() #Commented temporarily................................
    ROOT.mainloop()

if __name__ == "__main__":
    main(name = 'Sidhant', unique_id = "201888", code = "H3TH7A86")