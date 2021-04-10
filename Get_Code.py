#IMPORT HERE..
import Get_Details 
import tkinter as tk
import Fetch_Questions
import tkinter.font as tkfont

#DEFINE CONSTANTS HERE..
ROOT = None
ERROR_FONT = None
CODE_FONT1 = None
CODE_FONT2 = None

#INITIALISE GLOBAL VARIABLES HERE..
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
    code_submit.place(x = 140, y = 138)

def submit_code(event = None): #Button Function
    global code_text
    code = code_text.get("1.0","end-1c")
    if __name__ == "__main__":
        print(code)
    status = Fetch_Questions.fetch_questions(code)
    if status:
        window_close()
        Get_Details.get_details(code)
    else:
        error_label = tk.Label(ROOT, text = "The code you have entered is not valid!!",fg = 'red' , padx = 10, font = ERROR_FONT)
        error_label.place(x = 0, y = 113)
        if event != None:
            code_text.destroy()
            code_text = tk.Text(ROOT, height = 1, width = 24, font = CODE_FONT2, spacing1 = 5, spacing3 = 5)
            code_text.bind("<Return>", submit_code)
            code_text.place(x = 10, y = 60)
            code_text.insert("end-1c", code[:len(code)])

def define_constants():
    global ROOT, CODE_FONT1, CODE_FONT2, ERROR_FONT
    ROOT = tk.Tk()
    ROOT.minsize(407, 218)
    ROOT.protocol("WM_DELETE_WINDOW", window_close)
    ERROR_FONT = tkfont.Font(family = "Comic Sans MS", size = 10)
    CODE_FONT1 = tkfont.Font(family = "Comic Sans MS", size = 22)
    CODE_FONT2 = tkfont.Font(family = "Comic Sans MS", size = 20)

def get_code():
    define_constants()
    display_components()
    ROOT.mainloop()

if __name__ == "__main__":
    get_code()