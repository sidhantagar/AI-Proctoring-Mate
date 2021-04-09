#IMPORT HERE..
import tkinter as tk
import tkinter.font as tkfont

#DEFINE CONSTANTS HERE..
ROOT = tk.Tk()
CODE_FONT1 = tkfont.Font(family = "Comic Sans MS", size = 22)
CODE_FONT2 = tkfont.Font(family = "Comic Sans MS", size = 20)

#INITIALISE HERE
code_text = None
ROOT.minsize(407, 20)



def window_close():
    ROOT.destroy()
ROOT.protocol("WM_DELETE_WINDOW", window_close)

def display_components():
    global code_text
    code_label = tk.Label(ROOT, text = "Please enter the test code: ", padx = 10, font = CODE_FONT1)
    code_label.place(x = 0, y = 0)

    code_text = tk.Text(ROOT, height = 1, width = 24, font = CODE_FONT2, spacing1 = 5, spacing3 = 5)
    code_text.bind("<Return>", key_pressed)
    code_text.place(x = 10, y = 60)


    code_submit = tk.Button(ROOT, text = "Submit", padx = 3, pady = 0, height = 1, relief = 'raised', bd = 4, font = CODE_FONT2, command = submit_code)
    code_submit.place(x = 140, y = 120)

def key_pressed(event):
    submit_code()

def submit_code():
    text = code_text.get("1.0","end-1c")
    print(text)
    window_close()


def get_code():
    display_components()
    ROOT.mainloop()

if __name__ == "__main__":
    get_code()