import pandas as pd
import tkinter as tk
import tkinter.font as tkfont

#DEFINE CONSTANTS HERE..
DF_QUESTIONS = pd.read_csv('Questions.csv')
OPTION_FONT = tkfont.Font(family="Comic Sans MS",size=15)
QUESTION_FONT = tkfont.Font(family="Comic Sans MS",size=20)

#INITIALISE HERE...
variable = None
responses = None
select = None
calling_question = None

def selected():
    responses['Response'][calling_question] = variable.get()
    print("The option selected is "+ str(variable.get())) 

def extend_text(text):
    return text+(' '*(100-len(text)))

def view_question(question_frame, options_frame, option_var, this_question, df_responses, active_question):
    global select
    global variable
    global responses
    global calling_question 
    variable = option_var
    responses = df_responses
    calling_question= active_question
    question = tk.Label(question_frame, text = 'Q' + str(this_question['index'][0]+1) + '. ' + this_question['Question'][0], width = 50, padx = 10, pady = 10, anchor = 'nw', font = QUESTION_FONT)
    question.grid(row = 1, column = 1, sticky = 'W')
    op1 = tk.Radiobutton(options_frame, text = extend_text('A. '+this_question['Option_1'][0]), variable=option_var, value=1,command=selected, font = OPTION_FONT)
    op1.grid(row = 1, column = 1, sticky = 'W')
    op2 = tk.Radiobutton(options_frame, text = extend_text('B. '+this_question['Option_2'][0]), variable=option_var, value=2,command=selected, font = OPTION_FONT)
    op2.grid(row = 2, column = 1, sticky = 'W')
    op3 = tk.Radiobutton(options_frame, text = extend_text('C. '+this_question['Option_3'][0]), variable=option_var, value=3,command=selected, font = OPTION_FONT)
    op3.grid(row = 3, column = 1, sticky = 'W')
    op4 = tk.Radiobutton(options_frame, text = extend_text('D. '+this_question['Option_4'][0]), variable=option_var, value=4,command=selected, font = OPTION_FONT)
    op4.grid(row = 4, column = 1, sticky = 'W')
    variable.set(df_responses['Response'][active_question])

def button_1(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[0:1].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question(question_frame, options_frame, option_var, this_question, df_responses, 1)
def button_2(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[1:2].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 2)
def button_3(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[2:3].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 3)
def button_4(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[3:4].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 4)
def button_5(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[4:5].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 5)
def button_6(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[5:6].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 6)
def button_7(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[6:7].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 7)
def button_8(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[7:8].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 8)
def button_9(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[8:9].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 9)
def button_10(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[9:10].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 10)
def button_11(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[10:11].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 11)
def button_12(question_frame, options_frame, option_var, df_responses):
    this_question = DF_QUESTIONS[11:12].reset_index()[['index', 'Question', 'Option_1', 'Option_2', 'Option_3', 'Option_4']]
    view_question (question_frame, options_frame, option_var, this_question, df_responses, 12)