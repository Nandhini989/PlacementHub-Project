from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from students.forms import StudentRegistrationForm
from companies.forms import CompanyRegistrationForm
from colleges.forms import CollegeRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Redirect to profile completion based on role
            if user.role == 'student':
                return redirect('students:profile_complete')
            elif user.role == 'company':
                return redirect('companies:profile_complete')
            elif user.role == 'college':
                return redirect('colleges:profile_complete')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on role
            if user.role == 'student':
                return redirect('students:dashboard')
            elif user.role == 'company':
                return redirect('companies:dashboard')
            elif user.role == 'college':
                return redirect('colleges:dashboard')
            else:
                return redirect('landing_page')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('accounts:login')

@login_required
def landing_page(request):
    user = request.user
    context = {
        'user': user,
        'role': user.role,
    }
    return render(request, 'landing.html', context)
