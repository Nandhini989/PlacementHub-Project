from django.urls import path
from . import views

app_name = 'ai_tools'

urlpatterns = [
    path('resume/builder/', views.resume_builder, name='resume_builder'),
    path('resume/list/', views.resume_list, name='resume_list'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('interview/preparation/', views.interview_preparation, name='interview_preparation'),
    path('interview/session/<int:session_id>/', views.interview_session, name='interview_session'),
    path('interview/history/', views.interview_history, name='interview_history'),
]
