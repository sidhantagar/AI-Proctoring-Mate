import tkinter as tk
import tkinter.font as tkfont
from Verify_Details import verify_details
from Main import main
#DEFINE CONSTANTS HERE.. 
ROOT = None
WIDTH = None
ERROR_FONT = None
DETAILS_FONT1 = None
DETIALS_FONT2 = None

#INITIALISE HERE
name_text = None
id_text = None

def window_close():
    ROOT.destroy()

def switch_label(event):
    global name_text
    id_text.focus()
    name = name_text.get("1.0","end-1c")
    name_text.destroy()
    name_text = tk.Text(ROOT, height = 1, width = WIDTH, font = DETIALS_FONT2, spacing1 = 5, spacing3 = 5)
    name_text.bind("<Return>", switch_label)
    name_text.place(x = 10, y = 40)
    name_text.insert("end-1c", name[:len(name)])
    

def display_components():
    global name_text, id_text
    name_label = tk.Label(ROOT, text = "Please enter your name: ", padx = 10, font = DETAILS_FONT1)
    name_label.place(x = 0, y = 0)
    
    name_text = tk.Text(ROOT, height = 1, width = WIDTH, font = DETIALS_FONT2, spacing1 = 5, spacing3 = 5)
    name_text.bind("<Return>", switch_label)
    name_text.place(x = 10, y = 40)

    id_label = tk.Label(ROOT, text = "Please enter your (Unique ID/Reg No.): ", padx = 10, font = DETAILS_FONT1)
    id_label.place(x = 0, y = 100)

    id_text = tk.Text(ROOT, height = 1, width = WIDTH, font = DETIALS_FONT2, spacing1 = 5, spacing3 = 5)
    id_text.bind("<Return>", submit_details)
    id_text.place(x = 10, y = 140)

    details_submit = tk.Button(ROOT, text = "Submit", padx = 3, pady = 0, height = 1, relief = 'raised', bd = 4, font = DETIALS_FONT2, command = submit_details)
    details_submit.place(x = 170, y = 210)

def submit_details(event = None):
    global id_text
    name = name_text.get("1.0","end-1c")
    unique_id = id_text.get("1.0","end-1c")
    if __name__ == '__main__':
        print("Name : ", name)
    if __name__ == '__main__':
        print("Unique id : ", unique_id)
    valid = verify_details(unique_id)
    if valid:
        window_close()
        main(name, unique_id)
    else:
        error_label = tk.Label(ROOT, text = "The (Unique ID/Reg No.) you have entered is not valid!!",fg = 'red' , padx = 10, font = ERROR_FONT)
        error_label.place(x = 0, y = 190)
        if event != None:
            id_text.destroy()
            id_text = tk.Text(ROOT, height = 1, width = WIDTH, font = DETIALS_FONT2, spacing1 = 5, spacing3 = 5)
            id_text.bind("<Return>", submit_details)
            id_text.place(x = 10, y = 140)
            id_text.insert("end-1c", unique_id[:len(unique_id)])


def define_constants():
    global ROOT, DETAILS_FONT1, DETIALS_FONT2, WIDTH, ERROR_FONT
    WIDTH = 34
    ROOT = tk.Tk()
    ROOT.minsize(467, 275)
    ERROR_FONT = tkfont.Font(family = "Comic Sans MS", size = 10)
    DETAILS_FONT1 = tkfont.Font(family = "Comic Sans MS", size = 18)
    DETIALS_FONT2 = tkfont.Font(family = "Comic Sans MS", size = 16)
    ROOT.protocol("WM_DELETE_WINDOW", window_close)


def get_details():
    define_constants()
    display_components()
    ROOT.mainloop()

if __name__ == '__main__':
    get_details()