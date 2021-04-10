import random

randomizer = None

def shuffle_question_num(question_num, active_section):
    if randomizer is not None:
        return randomizer[active_section-1][question_num-1]

def define_initializations(DF_CONFIGURATION, NUM_QUESTIONS):
    global randomizer
    if (DF_CONFIGURATION.at['Randomize_questions','Value'] == 'True'):
        randomizer = []
        for i in NUM_QUESTIONS:
            arr = [j for j in range(1,i+1)]
            random.shuffle(arr)
            randomizer.append(arr)
    print(randomizer)

def initialze_shuffler(DF_CONFIGURATION, NUM_QUESTIONS):
    define_initializations(DF_CONFIGURATION, NUM_QUESTIONS)

