from django.shortcuts import render,redirect
from django.conf import settings
from django.urls import reverse
from django.template.loader import get_template
from django.http import HttpResponse

# import Models and utility
from django.contrib.auth.models import User
from Questions.models import *
from .models import *
from .utils import *


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from zipfile import ZipFile
import threading
import csv,codecs
import mimetypes
import os,glob
import zipfile
import shutil
import pandas as pd


################################################################################



# Added an e-mail thread.
# Used for faster mailing service.

class EmailThread(threading.Thread):

    def __init__(self,email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()





################################################################################





# For rendering the home page of our website.
# Rendering the Landing page.
def home_page(request):
    return render(request,'home_page.html')




################################################################################


# Student's UI Scrapper will collect the zip from this view.


def CollectMaterial(request):

    # This is risky!! - Note!!
    dir = settings.DELETABLE_ROOT+'/'
    for file in os.scandir(dir):
        os.remove(file.path)

    message = ''
    if(request.GET.get('error')=='True'):
        message = 'Test Code is Invalid!!'

    if(request.method == 'POST'):

        try:
            config = ConfigCreation.objects.filter(testCode = request.POST.get('code'))

            # Processing Work!!
            createPDF(request)
            processConfigurations(request)
            processQuestions(request)

            shutil.make_archive(settings.DELETABLE_ROOT+'/Question','zip',settings.FILES_ROOT+'/')

            # delete .csv files from the files directory!!
            dir = settings.FILES_ROOT+'/'
            for file in os.scandir(dir):
                os.remove(file.path)

            return redirect(reverse('download_files')+'?filepath='+ settings.DELETABLE_ROOT + '&file=Question.zip')

        except ConfigCreation.DoesNotExist:
            return redirect(reverse('collect_paper')+'?error=True')

    return render(request,'collect-1.html',{'message':message})





################################################################################


# View for Processing the Configurations.
# This view creates a .csv file for the Configuration Related to the testCode, fed by the Scrapper in the Input Field in front-end.

def processConfigurations(request):

    data = ConfigCreation.objects.get(testCode = request.POST.get('code'))

    section_2 = data.questionCountSec_2
    section_3 = data.questionCountSec_3
    pos_2 = data.positivesPerQuestionSec_2
    pos_3 = data.positivesPerQuestionSec_3
    neg_2 = data.negativesPerQuestionSec_2
    neg_3 = data.negativesPerQuestionSec_3

    if data.questionCountSec_2 is None:

        section_2 = 'NaN'
        pos_2 = 'NaN'
        neg_2 = 'NaN'

        section_3 = 'NaN'
        pos_3 = 'NaN'
        neg_3 = 'NaN'

    if data.questionCountSec_3 is None:

        section_3 = 'NaN'
        pos_3 = 'NaN'
        neg_3 = 'NaN'

    with open(settings.FILES_ROOT+'/Config.csv','w',newline='') as finp:

        fieldnames = ['Name','Value']
        writer = csv.DictWriter(finp,fieldnames = fieldnames)

        writer.writeheader()
        writer.writerow({'Name': 'Duration','Value': data.examDuration})
        writer.writerow({'Name': 'Calculator','Value': data.allowCalculator})
        writer.writerow({'Name': 'Id_format','Value': data.idFormat})
        writer.writerow({'Name': 'Num_questions_1','Value': data.questionCountSec_1})
        writer.writerow({'Name': 'Num_questions_2','Value': section_2})
        writer.writerow({'Name': 'Num_questions_3','Value': section_3})
        writer.writerow({'Name': 'Num_sections','Value': data.sectionCount})
        writer.writerow({'Name': 'Allow_keep_question','Value': data.keepQuestion})
        writer.writerow({'Name': 'Positive_per_question_1','Value': data.positivesPerQuestionSec_1})
        writer.writerow({'Name': 'Positive_per_question_2','Value': pos_2})
        writer.writerow({'Name': 'Positive_per_question_3','Value': pos_3})
        writer.writerow({'Name': 'Negative_per_question_1','Value': data.negativesPerQuestionSec_1})
        writer.writerow({'Name': 'Negative_per_question_2','Value': neg_2})
        writer.writerow({'Name': 'Negative_per_question_3','Value': neg_3})
        writer.writerow({'Name': 'Randomize_questions','Value':data.shuffleQuestions})
        writer.writerow({'Name': 'Randomize_options','Value':data.shuffleOptions})
        writer.writerow({'Name': 'Scheduled_Date','Value':data.scheduledDate})
        writer.writerow({'Name': 'Scheduled_Time','Value':data.scheduledTime})






################################################################################




# This Function will create the .csv file of All the questions in the Config, which has been requested by the user.
# .csv files will be created Section wise.


def processQuestions(request):

    data = QuestionModel.objects.filter(test_code = request.POST.get('code')).order_by('sectionNumber').order_by('questionNumber')

    for i in range(3):

        data_ = data.filter(sectionNumber = i+1)

        if len(data_) == 0 :
            continue

        else :

            with open(settings.FILES_ROOT+'/Questions_section'+ str(i+1) +'.csv','w',newline='') as finp:

                fieldnames = ['Question','Option_1','Option_2','Option_3','Option_4','Multicorrect']
                writer = csv.DictWriter(finp,fieldnames = fieldnames)

                writer.writeheader()

                for j in range(len(data_)):

                    data_filtered = data_.filter(questionNumber = j+1)

                    writer.writerow({
                        'Question' : data_filtered[0].question,
                        'Option_1' : data_filtered[0].option_1,
                        'Option_2' : data_filtered[0].option_2,
                        'Option_3' : data_filtered[0].option_3,
                        'Option_4' : data_filtered[0].option_4,
                        'Multicorrect' : data_filtered[0].isMultiCorrect
                    })
    print('Questions Saved successfully!!')







################################################################################



# This function creates a .pdf file consisting of all the questions in that test, placed at the same place.
# This pdf will be provided to the student,if the teacher sets the Keep Question Option for any test's Configuration.


def createPDF(request):

    context = {}
    code = request.POST.get('code')
    quiz_name = ConfigCreation.objects.get(testCode = code).quizName
    context['author'] = ConfigCreation.objects.get(testCode = code).testCreator
    context['name'] = quiz_name
    context['code'] = code
    context['duration'] = ConfigCreation.objects.get(testCode = code).examDuration
    context['sec1'] = True
    context['sec2'] = False
    context['sec3'] = False
    for i in range(3):

        obj = QuestionModel.objects.filter(test_code = ConfigCreation.objects.get(testCode = code))

        if(len(obj.filter(sectionNumber = i+1))):
            context['data'+str(i+1)] = obj.filter(sectionNumber = i+1)
        else:
            context['data'+str(i+1)] = []

    obj_ = ConfigCreation.objects.get(testCode = code)

    if(obj_.sectionCount>2):
        context['sec2'] = True
        context['sec3'] = True
    elif(obj_.sectionCount>1 and obj_.sectionCount<3):
        context['sec2'] = True

    # For POSITIVES.
    if(obj_.positivesPerQuestionSec_1):
        context['pos_1'] = obj_.positivesPerQuestionSec_1
    else:
        context['pos_1'] = 1

    if(obj_.positivesPerQuestionSec_2):
        context['pos_2'] = obj_.positivesPerQuestionSec_2
    else:
        context['pos_2'] = 1

    if(obj_.positivesPerQuestionSec_3):
        context['pos_3'] = obj_.positivesPerQuestionSec_3
    else:
        context['pos_3'] = 1

    # For NEGATIVES.
    if(obj_.negativesPerQuestionSec_1):
        context['neg_1'] = obj_.negativesPerQuestionSec_1
    else:
        context['neg_1'] = 0

    if(obj_.negativesPerQuestionSec_2):
        context['neg_2'] = obj_.negativesPerQuestionSec_2
    else:
        context['neg_2'] = 0

    if(obj_.negativesPerQuestionSec_3):
        context['neg_3'] = obj_.negativesPerQuestionSec_3
    else:
        context['neg_3'] = 0

    create_pdf('render_questions.html',context)






################################################################################




# This is the dashboard View For the user.
# This is also the landing page after the user log's in.


def DashboardView(request):

    name = request.user.username
    questionsCreated = 0
    tests_taken = 0

    quizzesCreated = len(ConfigCreation.objects.filter(testCreator = User.objects.get(username=name)))
    config_obj = ConfigCreation.objects.filter(testCreator = User.objects.get(username=name))

    for test in config_obj:
        if test.questionCountSec_1:
            questionsCreated += test.questionCountSec_1
        if test.questionCountSec_2:
            questionsCreated += test.questionCountSec_2
        if test.questionCountSec_3:
            questionsCreated += test.questionCountSec_3

        tests_taken += len(AnswerKey.objects.filter(test_code = test.testCode))


    return render(request,'dashboard.html',{
        'name':name,
        'quiz_count':quizzesCreated,
        'question_count' : questionsCreated,
        'tests_taken' : tests_taken
    })







################################################################################



# For displaying important activities of the teacher on the timeline



def TimelineView(request):

    name = request.user.username
    user = User.objects.get(username = name)
    objects = ConfigCreation.objects.filter(testCreator = user)

    list = []
    for object in objects:
        list.append(object)

    return render(request,'timeline.html',{
        'name':name,
        'data':list
    })







################################################################################




# For Diaplying the Quizzes formed till date.
# next -> Rendering questions in downloadable pdf files, so that the user can download the questions, if he wants.

def TestsCreatedView(request):

    name = request.user.username
    config_obj = ConfigCreation.objects.filter(testCreator = User.objects.get(username = name))

    list = []
    for object in config_obj:
        list.append(object)

    return render(request,'tests.html',{
        'name':name,
        'data':list
        })






################################################################################



# Helper for TestsCreatedView.
# Renders all the questions assosiated to the quiz in pdf format.

def ViewQuestions(request,code = None):

    context = {}
    quiz_name = ConfigCreation.objects.get(testCode = code).quizName
    context['author'] = request.user.username
    context['name'] = quiz_name
    context['code'] = code
    context['duration'] = ConfigCreation.objects.get(testCode = code).examDuration
    context['sec1'] = True
    context['sec2'] = False
    context['sec3'] = False
    for i in range(3):

        obj = QuestionModel.objects.filter(test_code = ConfigCreation.objects.get(testCode = code))

        if(len(obj.filter(sectionNumber = i+1))):
            context['data'+str(i+1)] = obj.filter(sectionNumber = i+1)
        else:
            context['data'+str(i+1)] = []

    obj_ = ConfigCreation.objects.get(testCode = code)

    if(obj_.sectionCount>2):
        context['sec2'] = True
        context['sec3'] = True
    elif(obj_.sectionCount>1 and obj_.sectionCount<3):
        context['sec2'] = True

    # For POSITIVES.
    if(obj_.positivesPerQuestionSec_1):
        context['pos_1'] = obj_.positivesPerQuestionSec_1
    else:
        context['pos_1'] = 1

    if(obj_.positivesPerQuestionSec_2):
        context['pos_2'] = obj_.positivesPerQuestionSec_2
    else:
        context['pos_2'] = 1

    if(obj_.positivesPerQuestionSec_3):
        context['pos_3'] = obj_.positivesPerQuestionSec_3
    else:
        context['pos_3'] = 1

    # For NEGATIVES.
    if(obj_.negativesPerQuestionSec_1):
        context['neg_1'] = obj_.negativesPerQuestionSec_1
    else:
        context['neg_1'] = 0

    if(obj_.negativesPerQuestionSec_2):
        context['neg_2'] = obj_.negativesPerQuestionSec_2
    else:
        context['neg_2'] = 0

    if(obj_.negativesPerQuestionSec_3):
        context['neg_3'] = obj_.negativesPerQuestionSec_3
    else:
        context['neg_3'] = 0

    pdf = render_to_pdf('render_questions.html',context)

    if pdf:
        response = HttpResponse(pdf,content_type='application/pdf')
        filename = ""
        if(len(quiz_name)):
            filename = quiz_name + '_'+ code +'.pdf'
        else:
            filename = request.user.username + '_' + code + '.pdf'
        content = "inline; filename={}".format(filename)
        response['Content-Disposition'] = content
        return response

    return HttpResponse("Page Not Found")






################################################################################





# Download files view will make the dowloader to ask for if, the scrapper wants to download the .zip file.
# For this to work, all the validations must suffice.



def DownloadFiles(request):

    file_path = request.GET.get('filepath')+'/'+request.GET.get('file')
    download_filename = 'Question.zip'

    with open(file_path,'rb') as file:

        response = HttpResponse(file.read(),content_type='application/zip')
        response['Content-Disposition'] = "attachment; filename={}".format(download_filename)
        return response





################################################################################





# For downloading Video Files of indivisual student.

def DownloadVideoFiles(request,filename=None):

    file_path = settings.MEDIA_ROOT+'/'+filename
    download_filename = filename

    with open(file_path,'rb') as file:

        response = HttpResponse(file.read(),content_type='application/zip')
        response['Content-Disposition'] = "attachment; filename={}".format(download_filename)
        return response





################################################################################




# User can contact Developers, via this view.


# For DEVELOPERS
def DeveloperContact(request):

    if request.method == "POST":

        author = request.user.username
        mail_subject = request.POST.get('subject')
        mail_message = request.POST.get('message')

        email_message = render_to_string('developer-feedback-mail-body.html',{
            'name' : 'Developers',
            'message' : mail_message,
            'author' : author
        })

        email = EmailMessage(
            mail_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            ['dcode711@gmail.com','sidhant11136@gmail.com','vivekrai5839@gmail.com']
        )

        EmailThread(email).start()

        return render(request,'mail_sent.html',{
            'feedback':False,
            'message':'Thanks for contacting us',
            'pre':'We will reach back to you ',
            'post':' as soon as possible!!'
        })


    return render(request,'developer-contact.html')







################################################################################




# User can give feedback to his/her students, from this view.


# For STUDENTS
def StudentContact(request):

    if request.method == "POST":

        studentName = request.POST.get('student_name')
        studentMail = request.POST.get('student_mail')
        mailSubject = request.POST.get('mail_subject')
        mailMessage = request.POST.get('mail_message')
        author = request.user.username

        email_message = render_to_string('student-feedback-mail-body.html',{
            'name' : studentName,
            'message' : mailMessage,
            'author' : author
        })

        email = EmailMessage(
            mailSubject,
            email_message,
            settings.EMAIL_HOST_USER,
            [studentMail]
        )

        EmailThread(email).start()

        return render(request,'mail_sent.html',{
            'feedback':True,
            'message':'Thanks for your feedback',
            'pre':'We will send your message to ',
            'student':studentName,
            'post':' as soon as possible!!'
        })

    return render(request,'student-contact.html')







################################################################################




# Landing page for the Response view of the students, that the teacher will see.



def ResponseView(request):

    name = request.user.username
    config_obj = ConfigCreation.objects.filter(testCreator = User.objects.get(username = name))

    list = []
    for object in config_obj:
        list.append(object)

    value = False
    if(request.GET.get('running') == 'True'):
        value = True

    return render(request,'response-page-1.html',{
        'name':name,
        'data':list,
        'running':value
        })







################################################################################



# Will give the specifics of the responses received for the test taken by the students.



def ResponseDetailsView(request,code=None):

    obj_ = ConfigCreation.objects.get(testCode = code)
    data = QuestionModel.objects.filter(test_code = code).order_by('sectionNumber').order_by('questionNumber')


    # IMPLEMENT THIS BUTTON FEATURE..

    # running = False
    # if(check_datetime(obj_.scheduledDate,obj_.scheduledTime,obj_.examDuration)):
    #     running = True

    # if(running):
    #     return redirect(reverse('response_page_1')+'?running=True')

    sec1_p = obj_.positivesPerQuestionSec_1
    sec2_p = obj_.positivesPerQuestionSec_2
    sec3_p = obj_.positivesPerQuestionSec_3

    sec1_n = obj_.negativesPerQuestionSec_1
    sec2_n = obj_.negativesPerQuestionSec_2
    sec3_n = obj_.negativesPerQuestionSec_3

    # Both values will be None, if any section is not present
    marking = [(sec1_p,sec1_n),(sec2_p,sec2_n),(sec3_p,sec3_n)]

    ans_list = []
    for i in range(3):

        temp = []
        data_ = data.filter(sectionNumber = i+1)

        if len(data_) == 0 :
            temp = [-711]

        else :

            for j in range(len(data_)):

                data_filtered = data_.filter(questionNumber = j+1)
                val = 0
                val += (data_filtered[0].ans_1)*1 + (data_filtered[0].ans_2)*2 + (data_filtered[0].ans_3)*4 + (data_filtered[0].ans_4)*8

                temp.append(val)

        ans_list.append(temp)

    responses = AnswerKey.objects.filter(test_code = code)
    final_context = []
    for response in responses:

        temp_dict = {}
        # student_metrics is a list of 10 elements [a,b,c,d,[sec1_mat],[sec2_mat],[sec3_mat],e,f,g,h]
        # a:section1_marks,b:section2_marks....,d:total_marks
        # e:sec1_max_marks...h:Total marks
        # we have to write evaluate_this

        student_metrics = evaluate_this(ans_list,pd.read_csv(response.responseFile),marking)
        student = Student.objects.get(Response = response)

        student.section1_marks = student_metrics[0]
        student.section1_total = student_metrics[7]
        if student_metrics[1] != "no" :
            student.section2_marks = student_metrics[1]
            student.section2_total = student_metrics[8]
        else:
            student.section2_marks = None
            student.section2_total = None
        if student_metrics[2] != "no":
            student.section3_marks = student_metrics[2]
            student.section3_total = student_metrics[9]
        else:
            student.section3_marks = None
            student.section3_total = None

        student.total_marks = student_metrics[3]
        student.overall_total = student_metrics[10]
        student.save()

        final_context.append(student)


    return render(request,'Response-page-2.html',{
        'quiz_name':obj_.quizName,
        'data':final_context,
        'sec_1': student_metrics[7],
        'sec_2': student_metrics[8],
        'sec_3': student_metrics[9],
        'total_marks': student_metrics[10]
    })





################################################################################



# Complete this for showing plot on the Web site.


# def OverallView(request,code=None):
#
#     try:
#         obj_ = ConfigCreation.objects.get(testCode = code)
#         responses_ = AnswerKey.objects.filter(test_code = code)
#         data = QuestionModel.objects.filter(test_code = code).order_by('sectionNumber').order_by('questionNumber')
#         metric_ = SectionMetrics.objects.get(test_code = obj_)
#         student = Student.objects.filter(test_code = code)
#
#         sec1 = obj_.questionCountSec_1
#         sec2 = obj_.questionCountSec_2
#         sec3 = obj_.questionCountSec_3
#
#         ans_list = []
#         for i in range(3):
#
#             temp = []
#             data_ = data.filter(sectionNumber = i+1)
#
#             if len(data_) == 0 :
#                 continue
#
#             else :
#                 for j in range(len(data_)):
#
#                     data_filtered = data_.filter(questionNumber = j+1)
#                     val = 0
#                     val += (data_filtered[0].ans_1)*1 + (data_filtered[0].ans_2)*2 + (data_filtered[0].ans_3)*4 + (data_filtered[0].ans_4)*8
#
#                     temp.append(val)
#
#             ans_list.append(temp)
#
#
#         response_list = []
#         student_names = []
#         student_id = []
#         for obj in responses_:
#             try:
#                 file = obj.responseFile
#                 response_list.append(pd.read_csv(file))
#                 student_names.append(obj.studentName)
#                 student_id.append(obj.studentId)
#             except:
#                 pass
#
#         metrics = []
#
#         metrics.append([0]*sec1) #solved
#         metrics.append([0]*sec1) #corr
#         metrics.append([0]*sec1) #incorr
#
#         if sec2:
#             metrics.append([0]*sec2)
#             metrics.append([0]*sec2)
#             metrics.append([0]*sec2)
#
#         if sec3:
#             metrics.append([0]*sec3)
#             metrics.append([0]*sec3)
#             metrics.append([0]*sec3)
#
#         evaluate_instance(metrics,response_list,ans_list,student_names,student_id,code)
#
#     except ConfigCreation.DoesNotExist:
#         print('Configuration Does not exists!!')
#
#     pass
