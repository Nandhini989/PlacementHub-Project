from django.urls import path
from . import views

app_name = 'colleges'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/complete/', views.profile_complete, name='profile_complete'),
    path('students/', views.students_list, name='students_list'),
    path('companies/', views.companies_list, name='companies_list'),
    path('analytics/', views.placement_analytics, name='placement_analytics'),
]
