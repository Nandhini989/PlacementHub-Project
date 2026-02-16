from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/complete/', views.profile_complete, name='profile_complete'),
    path('jobs/', views.job_listings, name='job_listings'),
    path('jobs/apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applications/', views.applications, name='applications'),
]
