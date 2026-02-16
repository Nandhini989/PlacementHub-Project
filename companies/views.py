from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import CompanyProfile
from .forms import CompanyRegistrationForm
from jobs.models import JobPost, Application

@login_required
def dashboard(request):
    if not request.user.is_company:
        return redirect('accounts:login')
    
    try:
        company_profile = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return redirect('companies:profile_complete')
    
    # Get company's job posts
    job_posts = JobPost.objects.filter(company=company_profile).order_by('-posted_at')[:5]
    
    # Get recent applications
    recent_applications = Application.objects.filter(job__company=company_profile).order_by('-applied_at')[:10]
    
    # Application statistics
    total_applications = Application.objects.filter(job__company=company_profile).count()
    shortlisted_count = Application.objects.filter(job__company=company_profile, status='shortlisted').count()
    selected_count = Application.objects.filter(job__company=company_profile, status='selected').count()
    
    context = {
        'company_profile': company_profile,
        'job_posts': job_posts,
        'recent_applications': recent_applications,
        'total_applications': total_applications,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
    }
    return render(request, 'companies/dashboard.html', context)

@login_required
def profile_complete(request):
    if not request.user.is_company:
        return redirect('accounts:login')
    
    try:
        company_profile = request.user.company_profile
        return redirect('companies:dashboard')
    except CompanyProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            company_profile = form.save(commit=False)
            company_profile.user = request.user
            company_profile.save()
            messages.success(request, 'Company profile completed successfully!')
            return redirect('companies:dashboard')
    else:
        form = CompanyRegistrationForm()
    
    return render(request, 'companies/profile_complete.html', {'form': form})

@login_required
def create_job(request):
    if not request.user.is_company:
        return redirect('accounts:login')
    
    try:
        company_profile = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return redirect('companies:profile_complete')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        skills_required = request.POST.get('skills_required')
        job_type = request.POST.get('job_type')
        location = request.POST.get('location')
        salary_min = request.POST.get('salary_min')
        salary_max = request.POST.get('salary_max')
        experience_required = request.POST.get('experience_required', 0)
        application_deadline = request.POST.get('application_deadline')
        
        JobPost.objects.create(
            company=company_profile,
            title=title,
            description=description,
            requirements=requirements,
            skills_required=skills_required,
            job_type=job_type,
            location=location,
            salary_min=salary_min if salary_min else None,
            salary_max=salary_max if salary_max else None,
            experience_required=experience_required,
            application_deadline=application_deadline
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('companies:manage_jobs')
    
    return render(request, 'companies/create_job.html', {'company_profile': company_profile})

@login_required
def manage_jobs(request):
    if not request.user.is_company:
        return redirect('accounts:login')
    
    try:
        company_profile = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return redirect('companies:profile_complete')
    
    jobs = JobPost.objects.filter(company=company_profile).order_by('-posted_at')
    
    context = {
        'company_profile': company_profile,
        'jobs': jobs,
    }
    return render(request, 'companies/manage_jobs.html', context)

@login_required
def job_applications(request, job_id):
    if not request.user.is_company:
        return redirect('accounts:login')
    
    try:
        company_profile = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return redirect('companies:profile_complete')
    
    job = get_object_or_404(JobPost, id=job_id, company=company_profile)
    applications = Application.objects.filter(job=job).order_by('-applied_at')
    
    context = {
        'company_profile': company_profile,
        'job': job,
        'applications': applications,
    }
    return render(request, 'companies/job_applications.html', context)

@login_required
def update_application_status(request, application_id, status):
    if not request.user.is_company:
        return redirect('accounts:login')
    
    try:
        company_profile = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return redirect('companies:profile_complete')
    
    application = get_object_or_404(Application, id=application_id, job__company=company_profile)
    application.status = status
    application.save()
    
    messages.success(request, f'Application status updated to {status}!')
    return redirect('companies:job_applications', job_id=application.job.id)
