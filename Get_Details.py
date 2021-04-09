import tkinter as tk
import tkinter.font as tkfont

#DEFINE CONSTANTS HERE..
WIDTH = 34
ROOT = tk.Tk()
CODE_FONT1 = tkfont.Font(family = "Comic Sans MS", size = 18)
CODE_FONT2 = tkfont.Font(family = "Comic Sans MS", size = 16)

#INITIALISE HERE
name_text = None
id_text = None
ROOT.minsize(467, 275)

def window_close():
    ROOT.destroy()
ROOT.protocol("WM_DELETE_WINDOW", window_close)

def display_components():
    global name_text, id_text
    name_label = tk.Label(ROOT, text = "Please enter your name: ", padx = 10, font = CODE_FONT1)
    name_label.place(x = 0, y = 0)
    
    name_text = tk.Text(ROOT, height = 1, width = WIDTH, font = CODE_FONT2, spacing1 = 5, spacing3 = 5)
    name_text.bind("<Return>", None)
    name_text.place(x = 10, y = 40)

    id_label = tk.Label(ROOT, text = "Please enter your (Unique ID/Reg No.): ", padx = 10, font = CODE_FONT1)
    id_label.place(x = 0, y = 110)

    id_text = tk.Text(ROOT, height = 1, width = WIDTH, font = CODE_FONT2, spacing1 = 5, spacing3 = 5)
    id_text.bind("<Return>", None)
    id_text.place(x = 10, y = 150)

    details_submit = tk.Button(ROOT, text = "Submit", padx = 3, pady = 0, height = 1, relief = 'raised', bd = 4, font = CODE_FONT2, command = submit_details)
    details_submit.place(x = 170, y = 205)

def submit_details():
    name = name_text.get("1.0","end-1c")
    print("Name : ", name)
    unique_id = id_text.get("1.0","end-1c")
    print("Unique id : ", unique_id)
    window_close()

def get_details():
    display_components()
    ROOT.mainloop()

if __name__ == '__main__':
    get_details()
    


