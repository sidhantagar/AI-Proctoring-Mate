import random

randomizer_questions = None
randomizer_options = None

def shuffle_question_num(question_num, active_section):
    if randomizer_questions is not None:
        return randomizer_questions[active_section-1][question_num-1]
    else:
        return question_num

def response_transform (number, question_num, active_section):
    if randomizer_options is None:
        return number
    response = 0 
    shuffling_pattern = randomizer_options[active_section-1][question_num-1]
    arr = [1,2,4,8]
    for i in range(4):
        vals = number % 2
        number = number//2
        response += vals*arr[shuffling_pattern[i]-1]
    return response

def response_inverse_transform (number, question_num, active_section):
    if randomizer_options is None:
        return number
    shuffling_pattern = randomizer_options[active_section-1][question_num-1]
    inverse_shuffling_pattern = [0, 0, 0, 0]
    response = 0 
    for i in range(4):
        inverse_shuffling_pattern[shuffling_pattern[i]-1]= i+1
    arr = [1,2,4,8]
    for i in range(4):
        vals = number % 2
        number = number//2
        response += vals*arr[shuffling_pattern[i]-1]
    return response


def shuffle_option (this_question, question_num, active_section):
    #print(this_question)
    shuffling_pattern = randomizer_options[active_section-1][question_num-1]
    shuffled_options = this_question.copy()
    for i in range(1,5):
        shuffled_options.at[0, 'Option_'+ str(i)] = this_question.at[0, 'Option_'+ str(shuffling_pattern[i-1])]
    #print(shuffled_options)
    #print(shuffling_pattern)
    return shuffled_options

def define_initializations(DF_CONFIGURATION, NUM_QUESTIONS):
    global randomizer_questions, randomizer_options
    if (DF_CONFIGURATION.at['Randomize_questions','Value'] == 'True'):
        randomizer_questions = []
        for i in NUM_QUESTIONS:
            arr = [j for j in range(1,i+1)]
            random.shuffle(arr)
            randomizer_questions.append(arr)
    if (DF_CONFIGURATION.at['Randomize_options','Value'] == 'True'):
        randomizer_options = []
        for i in NUM_QUESTIONS:
            temp = []
            for j in range(i):
                arr = [k for k in range(1,5)]
                random.shuffle(arr)
                temp.append(arr)
            randomizer_options.append(temp)
    #print(randomizer_options)
    #print(randomizer_questions)


def initialze_shuffler(DF_CONFIGURATION, NUM_QUESTIONS):
    define_initializations(DF_CONFIGURATION, NUM_QUESTIONS)
