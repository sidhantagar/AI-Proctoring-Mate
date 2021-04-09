from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('submitAnswers/',views.AnswerSubmission,name='answer_submission_page'),
    path('create/1/',login_required(views.Accessory),name='create_config_page'),
    path('create/2/',login_required(views.Questions),name='create_questions'),
    path('create/2/<int:section>/<int:questions>/<slug:id>/',login_required(views.AddQuestions),name='add_questions'),
    path('thanks/',login_required(views.ThanksView),name='thanks_view')
]
