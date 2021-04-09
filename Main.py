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


#INITIALISE HERE
cap = cv2.VideoCapture(0)
aud = pyaudio.PyAudio()
vid_frame_width = int(cap.get(3))
vid_frame_height = int(cap.get(4))
root = tk.Tk()
root.minsize(1200,800)
video_app_frame = tk.Frame(root, bg="white")
video_app_frame.place (x = 870, y = 10)
question_frame = tk.Frame(root, bg="white")
question_frame.place(x = 10, y = 10)
options_frame = tk.Frame(root)
options_frame.place(x = 10, y = 130)
navigation_frame = tk.Frame(root, bg="white")
navigation_frame.place(x = 870, y =400)
var = tk.IntVar()
option_Font = tkfont.Font(family="Comic Sans MS",size=15 )

import UI_Comp_Functions


question_Font = tkfont.Font(family="Comic Sans MS",size=20 )

#Pseudofunctions for UI components
def reset_config():
    b1 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.1', command = button_1, relief = 'raised', bd = 4)
    b1.grid(column = 1, row = 1, padx = 3, pady = 3)
    b2 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.2', command = button_2, relief = 'raised', bd = 4)
    b2.grid(column = 2, row = 1, padx = 3, pady = 3)
    b3 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.3', command = button_3, relief = 'raised', bd = 4)
    b3.grid(column = 3, row = 1, padx = 3, pady = 3)
    b4 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.4', command = button_4, relief = 'raised', bd = 4)
    b4.grid(column = 1, row = 2, padx = 3, pady = 3)
    b5 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.5', command = button_5, relief = 'raised', bd = 4)
    b5.grid(column = 2, row = 2, padx = 3, pady = 3)
    b6 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.6', command = button_6, relief = 'raised', bd = 4)
    b6.grid(column = 3, row = 2, padx = 3, pady = 3)
    b7 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.7', command = button_7, relief = 'raised', bd = 4)
    b7.grid(column = 1, row = 3, padx = 3, pady = 3)
    b8 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.8', command = button_8, relief = 'raised', bd = 4)
    b8.grid(column = 2, row = 3, padx = 3, pady = 3)
    b9 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.9', command = button_9, relief = 'raised', bd = 4)
    b9.grid(column = 3, row = 3, padx = 3, pady = 3)
    b10 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.10', command = button_10, relief = 'raised', bd = 4)
    b10.grid(column = 1, row = 4, padx = 3, pady = 3)
    b11 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.11', command = button_11, relief = 'raised', bd = 4)
    b11.grid(column = 2, row = 4, padx = 3, pady = 3)
    b12 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.12', command = button_12, relief = 'raised', bd = 4)
    b12.grid(column = 3, row = 4, padx = 3, pady = 3)

def button_1():
    reset_config()
    b1 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.1', command = button_1, relief = 'sunken', bd = 4)
    b1.grid(column = 1, row = 1, padx = 3, pady = 3)
    UI_Comp_Functions.button_1(question_frame, options_frame, var)
def button_2():
    reset_config()
    b2 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.2', command = button_2, relief = 'sunken', bd = 4)
    b2.grid(column = 2, row = 1, padx = 3, pady = 3)
    UI_Comp_Functions.button_2(question_frame, options_frame, var)
def button_3():
    reset_config()
    b3 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.3', command = button_3, relief = 'sunken', bd = 4)
    b3.grid(column = 3, row = 1, padx = 3, pady = 3)
    UI_Comp_Functions.button_3(question_frame, options_frame, var)
def button_4():
    reset_config()
    b4 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.4', command = button_4, relief = 'sunken', bd = 4)
    b4.grid(column = 1, row = 2, padx = 3, pady = 3)
    UI_Comp_Functions.button_4(question_frame, options_frame, var)
def button_5():
    reset_config()
    b5 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.5', command = button_5, relief = 'sunken', bd = 4)
    b5.grid(column = 2, row = 2, padx = 3, pady = 3)
    UI_Comp_Functions.button_5(question_frame, options_frame, var)
def button_6():
    reset_config()
    b6 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.6', command = button_6, relief = 'sunken', bd = 4)
    b6.grid(column = 3, row = 2, padx = 3, pady = 3)
    UI_Comp_Functions.button_6(question_frame, options_frame, var)
def button_7():
    reset_config()
    b7 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.7', command = button_7, relief = 'sunken', bd = 4)
    b7.grid(column = 1, row = 3, padx = 3, pady = 3)
    UI_Comp_Functions.button_7(question_frame, options_frame, var)
def button_8():
    reset_config()
    b8 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.8', command = button_8, relief = 'sunken', bd = 4)
    b8.grid(column = 2, row = 3, padx = 3, pady = 3)
    UI_Comp_Functions.button_8(question_frame, options_frame, var)
def button_9():
    reset_config()
    b9 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.9', command = button_9, relief = 'sunken', bd = 4)
    b9.grid(column = 3, row = 3, padx = 3, pady = 3)
    UI_Comp_Functions.button_9(question_frame, options_frame, var)
def button_10():
    reset_config()
    b10 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.10', command = button_10, relief = 'sunken', bd = 4)
    b10.grid(column = 1, row = 4, padx = 3, pady = 3)
    UI_Comp_Functions.button_10(question_frame, options_frame, var)
def button_11():
    reset_config()
    b11 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.11', command = button_11, relief = 'sunken', bd = 4)
    b11.grid(column = 2, row = 4, padx = 3, pady = 3)
    UI_Comp_Functions.button_11(question_frame, options_frame, var)
def button_12():
    reset_config()
    b12 = tk.Button(navigation_frame, padx = 3, pady = 3, width = 10, height = 3, text = 'Q.12', command = button_12, relief = 'sunken', bd = 4)
    b12.grid(column = 3, row = 4, padx = 3, pady = 3)
    UI_Comp_Functions.button_12(question_frame, options_frame, var)
def selected():
    print("The option selected is "+ str(var.get())) 



#INITIALISER FUNCTIONS
reset_config()
button_1()


#DYNAMIC COMPONENTS..
lmain = tk.Label(video_app_frame, anchor = 'ne')
lmain.grid(row = 1, column = 1)
status = tk.Label(video_app_frame, text = 'The status will show here!', font = option_Font, width = 27)
status.grid(row = 2, column = 1)

#DEFINE CONSTANTS HERE..
SUSPICIOUS_THRESHOLD = 0.5
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

#DEFINE BASIC VARIABLES HERE..
av_index = 1
stream = 0
recording = 0 
video_output = 0
audio_output = []

def record_if_suspicious(vid_frame,aud_frame):
    global recording
    global av_index
    global SUSPICIOUS_THRESHOLD
    global video_output
    global audio_output
    #get suspicious value here
    suspicious_value = 0.7
    #...
    if suspicious_value >= SUSPICIOUS_THRESHOLD:
        if recording == 0:
            video_output = cv2.VideoWriter('Video_'+str(av_index)+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (vid_frame_width,vid_frame_height))
            video_output.write(vid_frame)
            audio_output = []
            audio_output.append(aud_frame)
            recording = 1
        elif recording == 1:
            video_output.write(vid_frame)
            audio_output.append(aud_frame)
    else:
        if recording == 0:
            return
        elif recording == 1:
            video_output.write(vid_frame)
            audio_output.append(aud_frame)
            
            final_audio = ("Audio_"+str(av_index)+'.wav','wb')
            final_audio.setnchannels(CHANNELS)
            final_audio.setsampwidth(aud.get_sample_size(FORMAT))
            final_audio.setframerate(RATE)
            final_audio.writeframes(b''.join(audio_output))
            final_audio.close()

            video_output.release()
            av_index+=1
            recording = 0

def base_function():
    global root
    global stream
    ret, vid_frame = cap.read()
    stream = aud.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True, frames_per_buffer=CHUNK)
    aud_frame = stream.read(CHUNK)
    
    record_if_suspicious(vid_frame,aud_frame)

    imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv2.resize(vid_frame, (0, 0), fx = 0.5, fy = 0.5) , cv2.COLOR_BGR2RGBA)))
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, base_function)   
base_function()
root.mainloop()




final_audio = wave.open("Audio_"+str(av_index)+'.wav','wb')
final_audio.setnchannels(CHANNELS)
final_audio.setsampwidth(aud.get_sample_size(FORMAT))
final_audio.setframerate(RATE)
final_audio.writeframes(b''.join(audio_output))
final_audio.close()
video_output.release()

stream.stop_stream()
stream.close()

cap.release()
cv2.destroyAllWindows()