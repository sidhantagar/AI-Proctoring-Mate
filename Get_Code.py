#IMPORT HERE..
import os
import Get_Details
import Check_Datetime 
import tkinter as tk
import Fetch_Questions
import File_Mover_Remover
import tkinter.font as tkfont

#DEFINE CONSTANTS HERE..
ROOT = None
ERROR_FONT = None
CODE_FONT1 = None
CODE_FONT2 = None

#INITIALISE GLOBAL VARIABLES HERE..
practice_mode = None
code_text = None

def window_close():
    ROOT.destroy()

def display_components():
    global code_text
    code_label = tk.Label(ROOT, text = "Please enter the test code: ", padx = 10, font = CODE_FONT1)
    code_label.place(x = 0, y = 0)

    code_text = tk.Text(ROOT, height = 1, width = 24, font = CODE_FONT2, spacing1 = 5, spacing3 = 5)
    code_text.bind("<Return>", submit_code)
    code_text.place(x = 10, y = 60)

    code_submit = tk.Button(ROOT, text = "Submit", padx = 3, pady = 0, height = 1, relief = 'raised', bd = 4, font = CODE_FONT2, command = submit_code)
    code_submit.place(x = 140, y = 158)

    testmode_checkbox = tk.Checkbutton(ROOT, text = "Practice Mode", variable=practice_mode, onvalue=1,command=disable_textbox, font = ERROR_FONT)
    testmode_checkbox.place(x = 5, y = 112)

def disable_textbox():
    if practice_mode.get():
        code_text.configure(state="disabled", background= 'gray85')
    else:
        code_text.configure(state="normal", background= 'white')

def submit_code(event = None): #Button Function
    global code_text
    code = code_text.get("1.0","end-1c")
    if __name__ == "__main__":
        print(code)
    if practice_mode.get():
        window_close()
        Get_Details.get_details("PRACTICE")
        return
    if code == '':
        status = False
    else:
        status = Fetch_Questions.fetch_questions(code)
    if status == True:
        error_code = Check_Datetime.check_datetime(code)
        print(error_code)
    if status==1 and error_code == 3:
        window_close()
        Get_Details.get_details(code)
    else:
        if status== 0:
            error_label = tk.Label(ROOT, text = "The code you have entered is not valid!!",fg = 'red' , padx = 10, font = ERROR_FONT, width = 70, anchor = "nw")
            error_label.place(x = 0, y = 133) 
        elif error_code == 2:
            time_until_start = int(Check_Datetime.time_until_start(code))
            error_label = tk.Label(ROOT, text = "This test has not started yet! Please wait for "+ str (time_until_start) + " minutes.",fg = 'red' , padx = 10, font = ERROR_FONT, width = 70, anchor = "nw")
            error_label.place(x = 0, y = 133) 
        elif error_code == 1:
            error_label = tk.Label(ROOT, text = "Sorry, There is not enough time for you to attempt the test!!",fg = 'red' , padx = 10, font = ERROR_FONT, width = 70, anchor = "nw")
            error_label.place(x = 0, y = 133) 
        elif error_code == 0:
            error_label = tk.Label(ROOT, text = "The test is already over!!",fg = 'red' , padx = 10, font = ERROR_FONT, width = 70, anchor = "nw")
            error_label.place(x = 0, y = 133) 
        if event != None:
            code_text.destroy()
            code_text = tk.Text(ROOT, height = 1, width = 24, font = CODE_FONT2, spacing1 = 5, spacing3 = 5)
            code_text.bind("<Return>", submit_code)
            code_text.place(x = 10, y = 60)
            code_text.insert("end-1c", code[:len(code)])
        if status == True:
            File_Mover_Remover.remove_test_files(code)

def define_constants():
    global ROOT, CODE_FONT1, CODE_FONT2, ERROR_FONT
    ROOT = tk.Tk()
    ROOT.minsize(407, 235)
    ROOT.protocol("WM_DELETE_WINDOW", window_close)
    ERROR_FONT = tkfont.Font(family = "Comic Sans MS", size = 10)
    CODE_FONT1 = tkfont.Font(family = "Comic Sans MS", size = 22)
    CODE_FONT2 = tkfont.Font(family = "Comic Sans MS", size = 20)

def define_initializations():
    global practice_mode
    practice_mode = tk.IntVar()

def get_code():
    define_constants()
    define_initializations()
    display_components()
    ROOT.mainloop()

if __name__ == "__main__":
    get_code()