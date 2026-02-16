from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/complete/', views.profile_complete, name='profile_complete'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/manage/', views.manage_jobs, name='manage_jobs'),
    path('jobs/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('applications/<int:application_id>/update/<str:status>/', views.update_application_status, name='update_application_status'),
]
