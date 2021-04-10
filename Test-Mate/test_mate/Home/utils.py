from io import BytesIO,StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from urllib.request import urlopen
import datetime
import pandas as pd


#####################DATE##TIME##UTILITY#########################################################

def get_server_time():
    get_time = urlopen('http://just-the-time.appspot.com/')
    get_time = get_time.read().strip().decode('utf-8')
    date = [int (x) for x in (get_time.split(' ')[0]).split('-')]
    time = [int (x) for x in (get_time.split(' ')[1]).split(':')]
    datetime_today = datetime.datetime(date[0], date[1], date[2], time[0], time[1]) + datetime.timedelta(minutes= 325)
    return datetime_today

def get_end_time(date,time,duration):

    date = [int(x) for x in date.split('-')]
    time = [int(x) for x in time.split(":")]
    duration_ = int(duration)
    datetime_scheduled = datetime.datetime(date[0], date[1], date[2], time[0], time[1]) + datetime.timedelta(minutes= duration_)
    return datetime_scheduled

def check_datetime(date,time,duration):

    now = get_server_time()
    end = get_end_time(date,time,duration)

    print(end,now,(end-now).total_seconds())

    if ((end-now).total_seconds()) >= 0:
        return 1
    else:
        return 0


#####################PDF##UTILITY###########################################################



def render_to_pdf(template_source,context_dict = {}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type = 'application/pdf')
    return None

def create_pdf(template_source,context_dict = {}):

    template = get_template(template_source)
    html = template.render(context_dict)
    with open(settings.FILES_ROOT+'/Questions.pdf', 'wb+') as output:
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
    print('PDF created success!!')


###################EVALUATE##STUDENT##METRICS############################################################


def evaluate_this(ans_list,response_df,marking_list):
    student_metric = [0,0,0,0,[0,0,0],[0,0,0],[0,0,0],0,0,0,0]


    # Assume unattempted = 0

    val = 0   #for student's total
    val_ = 0  #for total
    for i in range(3):
        # i-section number

        if(ans_list[i][0] != -711):

            student_metric[i+7] = len(ans_list[i])*marking_list[i][0]
            val_ += student_metric[i+7]

            for j in range(len(ans_list[i])):
                # j - question number

                if(response_df.at[j,"Response_section_"+str(i+1)] > 0):
                    # student answered
                    student_metric[i+4][0] += 1
                    if(response_df.at[j,"Response_section_"+str(i+1)] == ans_list[i][j]):
                        # correct
                        student_metric[i+4][1] += 1
                        student_metric[i] += marking_list[i][0]
                    else:
                        # incorrect
                        student_metric[i+4][2] += 1  #for test metric section's incorrect update
                        student_metric[i] += marking_list[i][1]  #for marks Update
                else:
                    # unanswered question.
                    pass

        else:
            student_metric[i] = "no"

        if student_metric[i] and student_metric[i] != "no":
            val += student_metric[i]

    # total marks Update
    student_metric[3] = val
    student_metric[10] = student_metric[7] + student_metric[8] + student_metric[9]

    print(student_metric)

    return student_metric




#####################EVALUATE##FOR##SECTION##METRICS#######################################################




def evaluate_instance(metric,response_list,answer_list,student_names,student_id,code):

    # create metric for a test code
    for response in response_list:
        for section in range(len(metric)//3):
            for question in range(len(metric[section*3])):
                if response.at[question,"Response_section_"+str(section+1)]>0:
                    metric[3*section][question] += 1
                    if response.at[question,"Response_section_"+str(section+1)] == answer_list[section][question]:
                        metric[3*section+1][question] += 1
                    else:
                        metric[3*section+2][question] += 1

    # for id in student_id:
    #     student_ = Student.objects.filter(test_code = code).get(studentId = id)


    return metric




##########################UTILITY##FOR##SECTION##METRICS################################################



def list_to_str(lst):

    temp_list = []
    temp_list.append('[')
    for i in range (len(lst)-1):
        temp_list.append(str(lst[i])+', ')
    temp_list.append(str(lst[len(lst)-1]))
    temp_list.append(']')
    return "".join(temp_list)
