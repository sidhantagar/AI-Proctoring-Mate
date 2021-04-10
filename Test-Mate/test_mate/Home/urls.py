from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('',views.home_page,name='home_page'),
    path('CollectMaterial/',views.CollectMaterial,name='collect_paper'),
    path('dashboard/',login_required(views.DashboardView),name='dashboard_view'),
    path('dashboard/timeline/',login_required(views.TimelineView),name='user_timeline'),
    path('dashboard/tests/',login_required(views.TestsCreatedView),name='test_created'),
    path('dashboard/view/questions/<slug:code>/',login_required(views.ViewQuestions),name='view_questions'),
    path('CollectMaterial/download/',views.DownloadFiles,name='download_files'),
    path('dashboard/Contact/developers/',login_required(views.DeveloperContact),name='developer_contact'),
    path('dashboard/Contact/students/',login_required(views.StudentContact),name='student_contact'),
    path('dashboard/responses/',login_required(views.ResponseView),name='response_page_1'),
    path('dashboard/responses/1/<slug:code>/',login_required(views.ResponseDetailsView),name='response_page_2'),

]
