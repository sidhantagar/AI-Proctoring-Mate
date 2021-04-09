import pandas as pd
import tkinter as tk
import tkinter.font as tkfont


#INITIALISE HERE...
df_questions = pd.read_csv('Questions.csv')
option_Font = tkfont.Font(family="Comic Sans MS",size=15)
question_Font = tkfont.Font(family="Comic Sans MS",size=20)
variable = None

def selected():
    print("The option selected is "+ str(variable.get())) 

def extend_text(text):
    #print(len(text))
    return text+(' '*(100-len(text)))

def view_question(question_frame, options_frame, var, this_question):
    global variable
    variable = var
    question = tk.Label(question_frame, text = this_question['Question'][0],width = 50, padx = 10 , pady = 10, anchor = 'nw', font = question_Font)
    question.grid(row = 1, column = 1, sticky = 'W')
    op1 = tk.Radiobutton(options_frame, text = extend_text(this_question['Option_1'][0]), variable=var, value=1,command=selected, font = option_Font)
    op1.grid(row = 1, column = 1, sticky = 'W')
    op2 = tk.Radiobutton(options_frame, text = extend_text(this_question['Option_2'][0]), variable=var, value=2,command=selected, font = option_Font)
    op2.grid(row = 2, column = 1, sticky = 'W')
    op3 = tk.Radiobutton(options_frame, text = extend_text(this_question['Option_3'][0]), variable=var, value=3,command=selected, font = option_Font)
    op3.grid(row = 3, column = 1, sticky = 'W')
    op4 = tk.Radiobutton(options_frame, text = extend_text(this_question['Option_4'][0]), variable=var, value=4,command=selected, font = option_Font)
    op4.grid(row = 4, column = 1, sticky = 'W')
    op4.select()

def button_1(question_frame, options_frame, var):
    this_question = df_questions[0:1].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question(question_frame, options_frame, var, this_question)
def button_2(question_frame, options_frame, var):
    this_question = df_questions[1:2].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_3(question_frame, options_frame, var):
    this_question = df_questions[2:3].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_4(question_frame, options_frame, var):
    this_question = df_questions[3:4].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_5(question_frame, options_frame, var):
    this_question = df_questions[4:5].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_6(question_frame, options_frame, var):
    this_question = df_questions[5:6].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_7(question_frame, options_frame, var):
    this_question = df_questions[6:7].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_8(question_frame, options_frame, var):
    this_question = df_questions[7:8].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_9(question_frame, options_frame, var):
    this_question = df_questions[8:9].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_10(question_frame, options_frame, var):
    this_question = df_questions[9:10].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_11(question_frame, options_frame, var):
    this_question = df_questions[10:11].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)
def button_12(question_frame, options_frame, var):
    this_question = df_questions[11:12].reset_index()[['Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, var, this_question)