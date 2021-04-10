from django.shortcuts import render,redirect
from Home.models import Student
from django.contrib.auth.models import User
from .models import AnswerKey,ConfigCreation,QuestionModel
from .utils import *

from urllib.parse import urlencode
from django.urls import resolve
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from django.http import HttpResponse

import sys
import pytz
import uuid
import csv
import os



##################ANSWER##SUBMISSION####################################################################




# View to receive Submission (Responses) from the students.

# response-file-format : TestCode_fn-sn_id_response.csv
# Video-file-format : TestCode_fn-sn_id_video.zip


def AnswerSubmission(request):

    if request.method=="POST":

        answer_file = request.FILES['answer_file']
        ext_ = os.path.splitext(str(answer_file))[1]
        file_name = os.path.splitext(str(answer_file))[0]

        lst = file_name.split('_')

        # INFO
        code = lst[0]
        name = " ".join(lst[1].split('-'))
        id = lst[2]
        type = lst[3]   #either 'response' or 'video'.

        try:
            obj_ = ConfigCreation.objects.get(testCode=code)

            if(check_datetime(obj_.scheduledDate,obj_.scheduledTime,obj_.examDuration)):

                try:
                    code_ = AnswerKey.objects.filter(test_code = obj_).get(studentId = id)
                    # AnswerKey Object already exists
                    if(ext_ == '.csv'):
                        if(os.path.splitext(str(code_.responseFile))[1] == '.csv'):
                            # response file already submitted.
                            return redirect(reverse('answer_submission_page')+"?config_error=False&video_error=False&response_error=True")
                        else:
                            code_.responseFile = answer_file
                    elif(ext_ == '.zip'):
                        if(os.path.splitext(str(code_.VideoFile))[1] == '.zip'):
                            # Video file already submitted
                            return redirect(reverse('answer_submission_page')+"?config_error=False&video_error=True&response_error=False")
                        else:
                            code_.VideoFile = answer_file
                    code_.save()

                except AnswerKey.DoesNotExist:
                    # AnswerKey Object doesn't exists
                    file = AnswerKey()
                    student = Student()

                    file.test_code = obj_
                    file.studentName = name
                    file.studentId = id
                    if(ext_ == '.csv'):
                        file.responseFile = answer_file
                    elif(ext_ == '.zip'):
                        file.VideoFile = answer_file

                    file.save()

                    student.test_code = obj_
                    student.studentName = name
                    student.studentId = id
                    student.Response = file

                    student.save()
            else:
                return redirect(reverse('answer_submission_page')+"?timeup_error=True")

        except ConfigCreation.DoesNotExist:
            return redirect(reverse('answer_submission_page')+"?config_error=True&video_error=False&response_error=False")

        return render(request,'thanks-submit.html')


    return render(request,'answerSubmission.html',{
        'config_error': request.GET.get('config_error')=='True',
        'video_error': request.GET.get('video_error')=='True',
        'response_error': request.GET.get('response_error')=='True',
        'timeup_error': request.GET.get('timeup_error')=='True'
    })






#######################ACCESSORY#################################################################



# Configuration View stays here.

def Accessory(request):

    if request.method == "POST":

        # new config object initialised.
        config = ConfigCreation()

        config.testCreator = User.objects.filter(username = request.user.username)[0]
        # Initialisation
        allow_calculator = 'disabled'
        keep_question = False
        keep_answer = False
        shuffle_questions = False
        shuffle_options = False

        if(request.POST.get('calculator')):
            allow_calculator = 'normal'

        if(request.POST.get('keepQuestion')):
            keep_question = True

        if(request.POST.get('shuffle_question')):
            shuffle_questions = True

        if(request.POST.get('shuffle_option')):
            shuffle_options = True

        id_format = request.POST.get('IDformat')
        duration = int(request.POST.get('duration'))

        config.idFormat = id_format
        config.examDuration = duration

        config.scheduledDate = request.POST.get('date')
        config.scheduledTime = request.POST.get('time')

        date = ""
        for x in str(datetime.now().date()).split('-'):
            date = x + '-' + date

        date = date[0:len(date)-1]

        config.dateCreated = date
        config.timeCreated = str(datetime.now().time()).split('.')[0]

        config.keepQuestion = keep_question
        config.allowCalculator = allow_calculator

        config.quizName = request.POST.get('quiz_name')
        config.quizDescription = request.POST.get('quiz_desc')

        config.shuffleOptions = shuffle_options
        config.shuffleQuestions = shuffle_questions

        if(request.POST.get('numberOfQuestion')):
            # User didn't press the section button.

            config.sectionCount = 1;

            config.questionCountSec_1 = request.POST['numberOfQuestion']
            config.questionCountSec_2 = None
            config.questionCountSec_3 = None

            config.positivesPerQuestionSec_1 = request.POST['positives']
            config.positivesPerQuestionSec_2 = None
            config.positivesPerQuestionSec_3 = None

            config.negativesPerQuestionSec_1 = request.POST['negatives']
            config.negativesPerQuestionSec_2 = None
            config.negativesPerQuestionSec_3 = None

        else:
            # user pressed the Section button.

            if(request.POST.get('numberOfQuestion_3')):
                config.sectionCount = 3;

                config.questionCountSec_1 = request.POST['numberOfQuestion_1']
                config.questionCountSec_2 = request.POST['numberOfQuestion_2']
                config.questionCountSec_3 = request.POST['numberOfQuestion_3']

                config.positivesPerQuestionSec_1 = request.POST['pos_1']
                config.positivesPerQuestionSec_2 = request.POST['pos_2']
                config.positivesPerQuestionSec_3 = request.POST['pos_3']

                config.negativesPerQuestionSec_1 = request.POST['neg_1']
                config.negativesPerQuestionSec_2 = request.POST['neg_2']
                config.negativesPerQuestionSec_3 = request.POST['neg_3']

            elif(request.POST.get('numberOfQuestion_2')):

                config.sectionCount = 2;

                config.questionCountSec_1 = request.POST['numberOfQuestion_1']
                config.questionCountSec_2 = request.POST['numberOfQuestion_2']
                config.questionCountSec_3 = None

                config.positivesPerQuestionSec_1 = request.POST['pos_1']
                config.positivesPerQuestionSec_2 = request.POST['pos_2']
                config.positivesPerQuestionSec_3 = None

                config.negativesPerQuestionSec_1 = request.POST['neg_1']
                config.negativesPerQuestionSec_2 = request.POST['neg_2']
                config.negativesPerQuestionSec_3 = None

            else:

                config.sectionCount = 1;

                config.questionCountSec_1 = request.POST['numberOfQuestion_1']
                config.questionCountSec_2 = None
                config.questionCountSec_3 = None

                config.positivesPerQuestionSec_1 = request.POST['pos_1']
                config.positivesPerQuestionSec_2 = None
                config.positivesPerQuestionSec_3 = None

                config.negativesPerQuestionSec_1 = request.POST['neg_1']
                config.negativesPerQuestionSec_2 = None
                config.negativesPerQuestionSec_3 = None

        test_code = generateTestCode(8)
        config.testCode = test_code
        scrambled_test_code = scrammbleCode(test_code)
        slug = hideCode(scrambled_test_code)

        config.save()

        base_url = reverse('create_questions')
        q_string = urlencode({'id':slug,'code':str(uuid.uuid4())})
        url = '{}?{}'.format(base_url,q_string)
        return redirect(url)

    return render(request,'configInput.html')





##########################QUESTIONS##############################################################



# This is the Questions view

def Questions(request,key = None):

    key = request.GET.get('id')
    code = extractCode(key)
    code = unscrambleCode(code)

    config = ConfigCreation.objects.get(testCode = code)

    return redirect('add_questions',section = 1,questions = config.questionCountSec_1,id = scramble(code))





###########################ADD##QUESTIONS###########################################################





# view where question's POST request and redirect is processed.
# Add Question view starts here

def AddQuestions(request,section,questions,id):

    config = ConfigCreation.objects.get(testCode = descramble(id))
    count = config.sectionCount

    # Just process the post, and store it inside the database.
    # remember : if id is same for two objects, in db -> a new object won't be created in loop!! :)
    if(request.method == 'POST'):

        questionCount = 0
        if(section == 2):
            questionCount = config.questionCountSec_1
        elif(section == 3):
            questionCount = config.questionCountSec_2
        else:
            questionCount = config.questionCountSec_3

        for i in range(questionCount):

            quest = QuestionModel()

            quest.test_code = ConfigCreation.objects.get(testCode = descramble(id))

            quest.sectionNumber = section-1
            quest.questionNumber = i+1

            quest.question = request.POST.get('q'+str(i+1))

            quest.option_1 = request.POST.get('opA_'+str(i+1))
            quest.option_2 = request.POST.get('opB_'+str(i+1))
            quest.option_3 = request.POST.get('opC_'+str(i+1))
            quest.option_4 = request.POST.get('opD_'+str(i+1))

            if(request.POST.get(str(i+1)+'y')):
                quest.isMultiCorrect = True

            if(request.POST.get('q'+str(i+1)+'_a')):
                quest.ans_1 = True
            if(request.POST.get('q'+str(i+1)+'_b')):
                quest.ans_2 = True
            if(request.POST.get('q'+str(i+1)+'_c')):
                quest.ans_3 = True
            if(request.POST.get('q'+str(i+1)+'_d')):
                quest.ans_4 = True

            quest.save()
            print('Post saved for question : {}'.format(i+1))


    if(count < section):
        # work here to break the loop of POST request for the last section.
        return redirect(reverse('thanks_view')+'?code='+str(descramble(id)))

    lastSection = False
    question = 0
    positive = 0
    negative = 0

    if(count == section):
        lastSection = True

    if(section == 1):
        question = config.questionCountSec_1
        positive = config.positivesPerQuestionSec_1
        negative = config.negativesPerQuestionSec_1
    elif(section == 2):
        question = config.questionCountSec_2
        positive = config.positivesPerQuestionSec_2
        negative = config.negativesPerQuestionSec_2
    else:
        question = config.questionCountSec_3
        positive = config.positivesPerQuestionSec_3
        negative = config.negativesPerQuestionSec_3

    context = {
        'current_section': section,
        'new_section':section+1,
        'questions' : question,
        'test_id': id,
        'pos' : positive,
        'neg' : negative,
        'last_section' : lastSection
        }

    return render(request,'addQuestion-'+str(question)+'.html',context)






############################THANKS##VIEW##########################################################



# Thanks view starts here!!

def ThanksView(request):

    code = request.GET.get('code')

    return render(request,'thanks.html',{
        'context' : code
    })


##############################TEMPORARY##CREATE##CSV##FUNCTION##########################################################



def createCSV(config,test_code):

    section_2 = config.questionCountSec_2
    section_3 = config.questionCountSec_3
    pos_2 = config.positivesPerQuestionSec_2
    pos_3 = config.positivesPerQuestionSec_3
    neg_2 = config.negativesPerQuestionSec_2
    neg_3 = config.negativesPerQuestionSec_3

    if config.questionCountSec_2 is None:

        section_2 = 'NaN'
        pos_2 = 'NaN'
        neg_2 = 'NaN'

        section_3 = 'NaN'
        pos_3 = 'NaN'
        neg_3 = 'NaN'

    if config.questionCountSec_3 is None:

        section_3 = 'NaN'
        pos_3 = 'NaN'
        neg_3 = 'NaN'


    with open(settings.MEDIA_ROOT+'/'+test_code+'-config.csv','w',newline='') as finp:
        txt = csv.writer(finp,delimiter=',')
        data = [['Name','Value'],
                ['TestCode',config.testCode],
                ['Duration',config.examDuration],
                ['Calculator',config.allowCalculator],
                ['Id_format',config.idFormat],
                ['Allow_keep_question',config.keepQuestion],
                ['Allow_keep_answer',config.keepAnswer],
                ['Num_sections',config.sectionCount],
                ['Num_questions_1',config.questionCountSec_1],
                ['Num_questions_2',section_2],
                ['Num_questions_3',section_3],
                ['Positive_per_question_1',config.positivesPerQuestionSec_1],
                ['Positive_per_question_2',pos_2],
                ['Positive_per_question_3',pos_3],
                ['Negative_per_question_1',config.negativesPerQuestionSec_1],
                ['Negative_per_question_2',neg_2],
                ['Negative_per_question_3',neg_3],
                ['Shuffle_Questions',config.shuffleQuestions],
                ['Shuffle_Options',config.shuffleOptions]]

        txt.writerows(data)
