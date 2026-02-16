from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import StudentProfile
from .forms import StudentRegistrationForm
from jobs.models import JobPost, Application

@login_required
def dashboard(request):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    # Get available jobs
    available_jobs = JobPost.objects.filter(status='active').order_by('-posted_at')[:10]
    
    # Get student's applications
    applications = Application.objects.filter(student=student_profile).order_by('-applied_at')[:5]
    
    # Application statistics
    applied_count = Application.objects.filter(student=student_profile, status='applied').count()
    shortlisted_count = Application.objects.filter(student=student_profile, status='shortlisted').count()
    selected_count = Application.objects.filter(student=student_profile, status='selected').count()
    
    context = {
        'student_profile': student_profile,
        'available_jobs': available_jobs,
        'applications': applications,
        'applied_count': applied_count,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def profile_complete(request):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
        return redirect('students:dashboard')
    except StudentProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student_profile = form.save(commit=False)
            student_profile.user = request.user
            student_profile.save()
            messages.success(request, 'Profile completed successfully!')
            return redirect('students:dashboard')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'students/profile_complete.html', {'form': form})

@login_required
def job_listings(request):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    jobs = JobPost.objects.filter(status='active').order_by('-posted_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(company__company_name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'student_profile': student_profile,
        'jobs': jobs,
        'search_query': search_query,
    }
    return render(request, 'students/job_listings.html', context)

@login_required
def apply_job(request, job_id):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    job = get_object_or_404(JobPost, id=job_id, status='active')
    
    # Check if already applied
    if Application.objects.filter(job=job, student=student_profile).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('students:job_listings')
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '')
        
        Application.objects.create(
            job=job,
            student=student_profile,
            cover_letter=cover_letter
        )
        messages.success(request, 'Application submitted successfully!')
        return redirect('students:applications')
    
    return render(request, 'students/apply_job.html', {'job': job, 'student_profile': student_profile})

@login_required
def applications(request):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    applications = Application.objects.filter(student=student_profile).order_by('-applied_at')
    
    context = {
        'student_profile': student_profile,
        'applications': applications,
    }
    return render(request, 'students/applications.html', context)
