import pandas as pd
import tkinter as tk
import tkinter.font as tkfont

#DEFINE CONSTANTS HERE..
PADX = None
PADY = None
OPTION_FONT = None
QUESTION_FONT = None
CALCULATOR_FONT = None
CALCULATOR_BUTTON_WIDTH = None
CALCULATOR_BUTTON_FONT = None

#INITIALISE HERE...
single_choice_var = None
multiple_choice_var = None
responses = None
select = None
calc_textbox = None
calling_question = None
df_questions = None
active_section = None

def single_choice_set():
    responses['Response_section_' + str(active_section)][calling_question] = single_choice_var.get()
    #print("The option single_choice_set(): is "+ str(single_choice_var.get())) 

def multiple_choice_set():
    res = 0
    for i in multiple_choice_var:
        res += i.get()
    responses['Response_section_' + str(active_section)][calling_question] = res

def multiple_choice_restore(val):   #Restores the option entered earlier 
    for i in range(len(multiple_choice_var)):
        multiple_choice_var[i].set(pow(2,i)*(val%2))
        val//=2

def extend_text(text):
    return text+(' '*(100-len(text)))

def view_question(question_frame, options_frame, this_question, df_responses, active_question):
    global select, responses, calling_question 
    responses = df_responses
    calling_question= active_question
    question = tk.Label(question_frame, text = 'Q' + str(this_question['index'][0]+1) + '. ' + this_question['Question'][0], width = 50, padx = 10, pady = 10, anchor = 'nw', font = QUESTION_FONT)
    question.grid(row = 1, column = 1, sticky = 'W')
    if (this_question['Multicorrect'][0]== 'No'):
        op1 = tk.Radiobutton(options_frame, text = extend_text('A. '+this_question['Option_1'][0]), variable=single_choice_var, value=1,command=single_choice_set, font = OPTION_FONT)
        op1.grid(row = 1, column = 1, sticky = 'W')
        op2 = tk.Radiobutton(options_frame, text = extend_text('B. '+this_question['Option_2'][0]), variable=single_choice_var, value=2,command=single_choice_set, font = OPTION_FONT)
        op2.grid(row = 2, column = 1, sticky = 'W')
        op3 = tk.Radiobutton(options_frame, text = extend_text('C. '+this_question['Option_3'][0]), variable=single_choice_var, value=3,command=single_choice_set, font = OPTION_FONT)
        op3.grid(row = 3, column = 1, sticky = 'W')
        op4 = tk.Radiobutton(options_frame, text = extend_text('D. '+this_question['Option_4'][0]), variable=single_choice_var, value=4,command=single_choice_set, font = OPTION_FONT)
        op4.grid(row = 4, column = 1, sticky = 'W')
        single_choice_var.set(df_responses['Response_section_' + str(active_section)][active_question])
    elif (this_question['Multicorrect'][0] == 'Yes' ):
        op1 = tk.Checkbutton(options_frame, text = extend_text('A. '+this_question['Option_1'][0]), variable=multiple_choice_var[0], onvalue=1,command=multiple_choice_set, font = OPTION_FONT)
        op1.grid(row = 1, column = 1, sticky = 'W')
        op2 = tk.Checkbutton(options_frame, text = extend_text('B. '+this_question['Option_2'][0]), variable=multiple_choice_var[1], onvalue=2,command=multiple_choice_set, font = OPTION_FONT)
        op2.grid(row = 2, column = 1, sticky = 'W')
        op3 = tk.Checkbutton(options_frame, text = extend_text('C. '+this_question['Option_3'][0]), variable=multiple_choice_var[2], onvalue=4,command=multiple_choice_set, font = OPTION_FONT)
        op3.grid(row = 3, column = 1, sticky = 'W')
        op4 = tk.Checkbutton(options_frame, text = extend_text('D. '+this_question['Option_4'][0]), variable=multiple_choice_var[3], onvalue=8,command=multiple_choice_set, font = OPTION_FONT)
        op4.grid(row = 4, column = 1, sticky = 'W')
        multiple_choice_restore(df_responses['Response_section_' + str(active_section)][active_question])


def button_num(question_frame, options_frame, df_responses, question_num):
    this_question = df_questions[question_num-1 : question_num].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4', 'Multicorrect']]
    view_question(question_frame, options_frame, this_question, df_responses, question_num)


def display_calculator(navigation_frame_1):
    global calc_textbox
    calc_textbox = tk.Text(navigation_frame_1, height = 3, width = 31, font = CALCULATOR_FONT, spacing1 = 5, spacing3 = 5)
    calc_textbox.insert("end-1c","\n\n")
    calc_textbox.grid(column = 1, row = 1, columnspan = 4, padx = PADX, pady = PADY+2)
    calc_b1 = tk.Button(navigation_frame_1, text = '(', command = calculator_b1, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b1.grid(column = 1, row = 2, padx = PADX, pady = PADY)
    calc_b2 = tk.Button(navigation_frame_1, text = ')', command = calculator_b2, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b2.grid(column = 2, row = 2, padx = PADX, pady = PADY)
    calc_b3 = tk.Button(navigation_frame_1, text = '%', command = calculator_b3, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b3.grid(column = 3, row = 2, padx = PADX, pady = PADY)
    calc_b4 = tk.Button(navigation_frame_1, text = 'C', command = calculator_b4, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b4.grid(column = 4, row = 2, padx = PADX, pady = PADY)
    calc_b5 = tk.Button(navigation_frame_1, text = '7', command = calculator_b5, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b5.grid(column = 1, row = 3, padx = PADX, pady = PADY)
    calc_b6 = tk.Button(navigation_frame_1, text = '8', command = calculator_b6, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b6.grid(column = 2, row = 3, padx = PADX, pady = PADY)
    calc_b7 = tk.Button(navigation_frame_1, text = '9', command = calculator_b7, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b7.grid(column = 3, row = 3, padx = PADX, pady = PADY)
    calc_b8 = tk.Button(navigation_frame_1, text = '/', command = calculator_b8, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b8.grid(column = 4, row = 3, padx = PADX, pady = PADY)
    calc_b9 = tk.Button(navigation_frame_1, text = '4', command = calculator_b9, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b9.grid(column = 1, row = 4, padx = PADX, pady = PADY)
    calc_b10 = tk.Button(navigation_frame_1, text = '5', command = calculator_b10, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b10.grid(column = 2, row = 4, padx = PADX, pady = PADY)
    calc_b11 = tk.Button(navigation_frame_1, text = '6', command = calculator_b11, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b11.grid(column = 3, row = 4, padx = PADX, pady = PADY)
    calc_b12 = tk.Button(navigation_frame_1, text = 'x', command = calculator_b12, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b12.grid(column = 4, row = 4, padx = PADX, pady = PADY)
    calc_b13 = tk.Button(navigation_frame_1, text = '1', command = calculator_b13, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b13.grid(column = 1, row = 5, padx = PADX, pady = PADY)
    calc_b14 = tk.Button(navigation_frame_1, text = '2', command = calculator_b14, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b14.grid(column = 2, row = 5, padx = PADX, pady = PADY)
    calc_b15 = tk.Button(navigation_frame_1, text = '3', command = calculator_b15, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b15.grid(column = 3, row = 5, padx = PADX, pady = PADY)
    calc_b16 = tk.Button(navigation_frame_1, text = '-', command = calculator_b16, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b16.grid(column = 4, row = 5, padx = PADX, pady = PADY)
    calc_b17 = tk.Button(navigation_frame_1, text = '.', command = calculator_b17, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b17.grid(column = 1, row = 6, padx = PADX, pady = PADY)
    calc_b18 = tk.Button(navigation_frame_1, text = '0', command = calculator_b18, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b18.grid(column = 2, row = 6, padx = PADX, pady = PADY)
    calc_b19 = tk.Button(navigation_frame_1, text = '=', command = calculator_b19, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b19.grid(column = 3, row = 6, padx = PADX, pady = PADY)
    calc_b20 = tk.Button(navigation_frame_1, text = '+', command = calculator_b20, relief = 'raised', bd = 4, font = CALCULATOR_BUTTON_FONT, width =  CALCULATOR_BUTTON_WIDTH, height = HEIGHT, padx = PADX+6)
    calc_b20.grid(column = 4, row = 6, padx = PADX, pady = PADY)
    calc_label = tk.Label(navigation_frame_1, text = 'For power function use xx operator', font = CALCULATOR_FONT, fg = "red")
    calc_label.grid(column = 1, row = 7, columnspan = 4, padx = PADX, sticky = 'nw' )
    calc_label = tk.Label(navigation_frame_1, text = 'eg: 4xx2 = 16', font = CALCULATOR_FONT, fg = "red")
    calc_label.grid(column = 1, row = 8, columnspan = 4, padx = PADX, sticky = 'nw' )

def calculator_justify():
    calc_textbox.tag_configure('center', justify = 'right')
    calc_textbox.tag_add('center', 1.0, "end")
    calc_textbox.configure(state = 'disabled')
def calculator_b1():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "(")
    calculator_justify()
def calculator_b2():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", ")")
    calculator_justify()
def calculator_b3():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "%")
    calculator_justify()
def calculator_b4():
    calc_textbox.configure(state = 'normal')
    calc_textbox.delete("1.0", "end-1c")
    calc_textbox.insert("end-1c", "\n\n")
def calculator_b5():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "7")
    calculator_justify()
def calculator_b6():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "8")
    calculator_justify()
def calculator_b7():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "9")
    calculator_justify()
def calculator_b8():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "/")
    calculator_justify()
def calculator_b9():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "4")
    calculator_justify()
def calculator_b10():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "5")
    calculator_justify()
def calculator_b11():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "6")
    calculator_justify()
def calculator_b12():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "x")
    calculator_justify()
def calculator_b13():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "1")
    calculator_justify()
def calculator_b14():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "2")
    calculator_justify()
def calculator_b15():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "3")
    calculator_justify()
def calculator_b16():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "-")
    calculator_justify()
def calculator_b17():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", ".")
    calculator_justify()
def calculator_b18():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "0")
    calculator_justify()
def calculator_b19():
    calc_textbox.configure(state = 'normal')
    strings = calc_textbox.get("1.0","end-1c").replace("x", "*").split("\n")
    calc_textbox.delete("1.0", "end-1c")
    calc_textbox.insert("end-1c", "\n".join(strings[2:]))
    try:
        result = eval(strings[-1])
    except:
        result = "Nan"
    if __name__ == "__main__":
        print(result)
    calc_textbox.insert("end-1c", "\n"+str(result)+"\n")
    calculator_justify()
def calculator_b20():
    calc_textbox.configure(state = 'normal')
    calc_textbox.insert("end-1c", "+")
    calculator_justify()

def define_constants():
    global df_questions, OPTION_FONT, QUESTION_FONT, CALCULATOR_FONT, CALCULATOR_BUTTON_WIDTH, CALCULATOR_BUTTON_FONT, PADX, PADY, HEIGHT
    PADX = 1
    PADY = 1
    HEIGHT = 1
    CALCULATOR_BUTTON_WIDTH = 5
    OPTION_FONT = tkfont.Font(family="Comic Sans MS",size=15)
    QUESTION_FONT = tkfont.Font(family="Comic Sans MS",size=20)
    CALCULATOR_FONT = tkfont.Font(family = "Comic Sans MS", size = 12)
    CALCULATOR_BUTTON_FONT = tkfont.Font(family = "Comic Sans MS", size = 13)

def define_initializations():
    global single_choice_var, multiple_choice_var
    single_choice_var = tk.IntVar()
    multiple_choice_var = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]

def select_question_set(section):
    global df_questions, active_section
    if  __name__ == '__main__':
        print("loading" + str(section) + "set")
    active_section = section
    df_questions = pd.read_csv('./Question/Questions_section'+ str(section) +'.csv')

def initialize_ui_components():
    define_constants()
    define_initializations()

def display_warning(warining_code, ROOT):
    ROOT.focus_force()
    ROOT.focus_set()
    ROOT.attributes('-topmost', True)

    if warining_code == 1:
        warning_label = tk.Label(ROOT, text = "This is a warning!! Please do not try to navigate away from the window else your \ntest will be ended", fg = 'red', padx = 10, font = QUESTION_FONT)
        warning_label.place(x = 15, y = 600,)
    return warning_label
        

if __name__ == '__main__':
    ROOT = tk.Tk()
    define_constants()
    define_initializations()
    select_question_set(1)
    ROOT.minsize(1400,800)
    ROOT.protocol("WM_DELETE_WINDOW", ROOT.destroy)
    navigation_frame_1 = tk.Frame(ROOT)
    navigation_frame_1.place(x = 1070, y = 380)
    display_calculator(navigation_frame_1)
    ROOT.mainloop()