#IMPORT HERE..
import Main
import pandas as pd
import tkinter as tk
import tkinter.font as tkfont

#DEFINE CONSTANTS HERE..
ROOT = None
DURATION = None
NAME = None
UNIQUE_ID = None
CODE = None
HEADING_FONT = None
INSTRUCTION_FONT = None
SUBINSTRUCTION_FONT = None
DF_CONFIGURATION = None

#INITIALISE GLOBAL VARIABLES HERE..
time_lapsed = None
timer_label = None
instructions_frame = None

def define_constants(name, unique_id, code):
    global ROOT, DURATION, NAME, UNIQUE_ID, CODE, DF_CONFIGURATION, INSTRUCTION_FONT, HEADING_FONT, SUBINSTRUCTION_FONT
    ROOT = tk.Tk()
    ROOT.minsize(1000, 800)
    ROOT['bg'] = "gray13"      #Termorarily changed to black theme :P 
    ROOT.protocol("WM_DELETE_WINDOW", window_close)
    DURATION = 90
    NAME = name
    UNIQUE_ID = unique_id
    CODE = code
    DF_CONFIGURATION = pd.read_csv("./Question/" + CODE + "/Config.csv").set_index("Name")[['Value']]
    HEADING_FONT = tkfont.Font(family = "Comic Sans MS", size = 20)
    INSTRUCTION_FONT = tkfont.Font(family = "Comic Sans MS", size = 15)
    SUBINSTRUCTION_FONT = tkfont.Font(family = "Comic Sans MS", size = 12)

def define_initializations():
    global time_lapsed, instructions_frame
    time_lapsed = 0
    instructions_frame = tk.Frame()
    instructions_frame.place(x = 15, y = 70)

def window_close():
    ROOT.destroy()

def show_timer():
    global time_lapsed, timer_label
    if time_lapsed == DURATION:
        window_close()
        Main.main(name = NAME, unique_id = UNIQUE_ID, code = CODE)
    if __name__ == '__main__':
        print(time_lapsed)
    time_lapsed = time_lapsed + 1
    timer_label = tk.Label(ROOT, text = "Time Remaining: "+str("%0*d" % (2, ((DURATION-time_lapsed)//60)))+":"+ str("%0*d" % (2, ((DURATION-time_lapsed)%60))), fg = 'red', width = 18 , font = INSTRUCTION_FONT)
    timer_label.place(x = 750, y = 10)
    timer_label.after(1000, show_timer)

def display_instructions():
    instruction_label = tk.Label(ROOT, text = "Instructions for the test: ", fg = 'black', padx = 10, font = HEADING_FONT)
    instruction_label.place(x = 15, y = 15)
    instruction_1 = tk.Label(instructions_frame, text = "Please read the following instructions carefully! Your test will start automatically when the timer \n runs out. DO NOT CLOSE THIS WINDOW!!                                                                                  ", fg = 'red', padx = 10, font = INSTRUCTION_FONT)
    instruction_1.pack(pady = 10)
    time_instruction = tk.Label(instructions_frame, text = "1. The total time alloted for this test is: " + str(DF_CONFIGURATION.at['Duration', 'Value']) + " Minutes", fg = 'black', padx = 10, font = INSTRUCTION_FONT)
    time_instruction.pack(anchor = 'w')
    autosubmit_instruction = tk.Label(instructions_frame, text = "2. Once the alloted time for the test runs out, your test will end automatically. You can see the remaining\n time at top right hand corner.\t\t\t\t\t\t\t          ", fg = 'black', padx = 10, font = INSTRUCTION_FONT)
    autosubmit_instruction.pack(anchor = 'w')
    if DF_CONFIGURATION.at['Calculator', 'Value'] == 'normal':
        calculator_instruction = tk.Label(instructions_frame, text = "3. The use of calculator is permitted for this test and is provided in the interface itself.", fg = 'black', padx = 10, font = INSTRUCTION_FONT)
    else:
        calculator_instruction = tk.Label(instructions_frame, text = "3. The use of calculator is not permitted for this test.", fg = 'black', padx = 10, font = INSTRUCTION_FONT)
    calculator_instruction.pack(anchor = 'w')
    close_instruction = tk.Label(instructions_frame, text = "4. DO NOT close the interface window else your test will be ended automatically.", fg = 'black', padx = 10, font = INSTRUCTION_FONT)
    close_instruction.pack(anchor = 'w')
    choice_instruction = tk.Label(instructions_frame, text = "5. All questions are in the form of MCQ with either ONE or MULTIPLE CHOICES as correct.", fg = 'black', padx = 10, font = INSTRUCTION_FONT)
    choice_instruction.pack(anchor = 'w')
    section_instruction = tk.Label(instructions_frame, text = "6. There are a total of " + str(DF_CONFIGURATION.at['Num_sections', 'Value']) + " section(s) in the test.", fg = 'black', padx = 10, font = INSTRUCTION_FONT)
    section_instruction.pack(anchor = 'w')
    # add extra instructions here!!
    for i in range(1, int(DF_CONFIGURATION.at['Num_sections', 'Value'])+1):
        load_section_details(i)

def load_section_details(section_num):
    section_number_instruction = tk.Label(instructions_frame, text = str(6 + section_num) +". The details for section number: " + str(section_num) + " are as follows:", fg = 'black', padx = 10, font = INSTRUCTION_FONT)
    section_number_instruction.pack(anchor = 'w')
    questions_instruction = tk.Label(instructions_frame, text = "\ti. The number of questions in this section are " + str(DF_CONFIGURATION.at["Num_questions_"+str(section_num), "Value"]) , fg = 'black', padx = 10, font = SUBINSTRUCTION_FONT)
    questions_instruction.pack(anchor = 'w')
    positive_instruction = tk.Label(instructions_frame, text = "\tii. Each correct answer this section will award " + str(DF_CONFIGURATION.at["Positive_per_question_"+str(section_num), "Value"]) + " marks", fg = 'black', padx = 10, font = SUBINSTRUCTION_FONT)
    positive_instruction.pack(anchor = 'w')
    if (str(DF_CONFIGURATION.at["Negative_per_question_"+str(section_num), "Value"]) != "0"):
        negative_instruction = tk.Label(instructions_frame, text = "\tiii. Each incorrect answer this section will attract a penalty of " + str(DF_CONFIGURATION.at["Negative_per_question_"+str(section_num), "Value"]) + " marks", fg = 'black', padx = 10, font = SUBINSTRUCTION_FONT)
    else:
        negative_instruction = tk.Label(instructions_frame, text = "\tiii. There is no penalty for incorrect answers in this section. ", fg = 'black', padx = 10, font = SUBINSTRUCTION_FONT)
    negative_instruction.pack(anchor = 'w')

def instruction_menu(name, unique_id, code):
    define_constants(name, unique_id, code)
    define_initializations()
    show_timer()
    display_instructions()
    ROOT.mainloop()

if __name__ == '__main__':
    instruction_menu(name = 'Sidhant Agarwal', unique_id = "20188028", code = "3uibkub")