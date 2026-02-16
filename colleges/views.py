from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import CollegeProfile
from .forms import CollegeRegistrationForm
from students.models import StudentProfile
from companies.models import CompanyProfile
from jobs.models import JobPost, Application

@login_required
def dashboard(request):
    if not request.user.is_college:
        return redirect('accounts:login')
    
    try:
        college_profile = request.user.college_profile
    except CollegeProfile.DoesNotExist:
        return redirect('colleges:profile_complete')
    
    # Get registered students from this college
    registered_students = StudentProfile.objects.filter(college_name__icontains=college_profile.college_name)
    
    # Get registered companies
    registered_companies = CompanyProfile.objects.all()
    
    # Get placement statistics
    total_applications = Application.objects.filter(student__in=registered_students).count()
    selected_students = Application.objects.filter(student__in=registered_students, status='selected').count()
    
    # Get recent activity
    recent_applications = Application.objects.filter(student__in=registered_students).order_by('-applied_at')[:10]
    
    # Top companies hiring from this college
    top_companies = Application.objects.filter(
        student__in=registered_students, 
        status='selected'
    ).values('job__company__company_name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    context = {
        'college_profile': college_profile,
        'registered_students': registered_students,
        'registered_companies': registered_companies,
        'total_applications': total_applications,
        'selected_students': selected_students,
        'recent_applications': recent_applications,
        'top_companies': top_companies,
    }
    return render(request, 'colleges/dashboard.html', context)

@login_required
def profile_complete(request):
    if not request.user.is_college:
        return redirect('accounts:login')
    
    try:
        college_profile = request.user.college_profile
        return redirect('colleges:dashboard')
    except CollegeProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = CollegeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            college_profile = form.save(commit=False)
            college_profile.user = request.user
            college_profile.save()
            messages.success(request, 'College profile completed successfully!')
            return redirect('colleges:dashboard')
    else:
        form = CollegeRegistrationForm()
    
    return render(request, 'colleges/profile_complete.html', {'form': form})

@login_required
def students_list(request):
    if not request.user.is_college:
        return redirect('accounts:login')
    
    try:
        college_profile = request.user.college_profile
    except CollegeProfile.DoesNotExist:
        return redirect('colleges:profile_complete')
    
    students = StudentProfile.objects.filter(college_name__icontains=college_profile.college_name)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(full_name__icontains=search_query) |
            Q(branch__icontains=search_query) |
            Q(skills__icontains=search_query)
        )
    
    context = {
        'college_profile': college_profile,
        'students': students,
        'search_query': search_query,
    }
    return render(request, 'colleges/students_list.html', context)

@login_required
def companies_list(request):
    if not request.user.is_college:
        return redirect('accounts:login')
    
    try:
        college_profile = request.user.college_profile
    except CollegeProfile.DoesNotExist:
        return redirect('colleges:profile_complete')
    
    companies = CompanyProfile.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        companies = companies.filter(
            Q(company_name__icontains=search_query) |
            Q(industry_type__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'college_profile': college_profile,
        'companies': companies,
        'search_query': search_query,
    }
    return render(request, 'colleges/companies_list.html', context)

@login_required
def placement_analytics(request):
    if not request.user.is_college:
        return redirect('accounts:login')
    
    try:
        college_profile = request.user.college_profile
    except CollegeProfile.DoesNotExist:
        return redirect('colleges:profile_complete')
    
    # Get students from this college
    students = StudentProfile.objects.filter(college_name__icontains=college_profile.college_name)
    
    # Placement statistics by branch
    branch_stats = Application.objects.filter(
        student__in=students, 
        status='selected'
    ).values('student__branch').annotate(
        total_students=Count('student__id', distinct=True),
        placed_students=Count('id', distinct=True)
    ).order_by('student__branch')
    
    # Company-wise placement
    company_stats = Application.objects.filter(
        student__in=students, 
        status='selected'
    ).values('job__company__company_name').annotate(
        placed_count=Count('id', distinct=True)
    ).order_by('-placed_count')[:10]
    
    # Job type statistics
    job_type_stats = Application.objects.filter(
        student__in=students, 
        status='selected'
    ).values('job__job_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'college_profile': college_profile,
        'branch_stats': branch_stats,
        'company_stats': company_stats,
        'job_type_stats': job_type_stats,
    }
    return render(request, 'colleges/placement_analytics.html', context)
