from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Resume, InterviewQuestion, InterviewSession, SessionQuestion
from students.models import StudentProfile
from companies.models import CompanyProfile

@login_required
def resume_builder(request):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    if request.method == 'POST':
        title = request.POST.get('title', 'Professional Resume')
        
        # Generate AI resume content based on student profile
        resume_content = generate_resume_content(student_profile)
        
        resume = Resume.objects.create(
            student=student_profile,
            title=title,
            content=resume_content
        )
        
        messages.success(request, 'Resume generated successfully!')
        return redirect('ai_tools:resume_list')
    
    return render(request, 'ai_tools/resume_builder.html', {'student_profile': student_profile})

@login_required
def resume_list(request):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    resumes = Resume.objects.filter(student=student_profile).order_by('-generated_at')
    
    return render(request, 'ai_tools/resume_list.html', {
        'student_profile': student_profile,
        'resumes': resumes
    })

@login_required
def resume_detail(request, resume_id):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    resume = get_object_or_404(Resume, id=resume_id, student=student_profile)
    
    return render(request, 'ai_tools/resume_detail.html', {
        'student_profile': student_profile,
        'resume': resume
    })

@login_required
def interview_preparation(request):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    companies = CompanyProfile.objects.all()
    
    if request.method == 'POST':
        company_id = request.POST.get('company')
        job_role = request.POST.get('job_role', '')
        
        company = None
        if company_id:
            company = get_object_or_404(CompanyProfile, id=company_id)
        
        # Create interview session
        session = InterviewSession.objects.create(
            student=student_profile,
            company=company,
            job_role=job_role
        )
        
        # Generate and add questions
        questions = generate_interview_questions(company, job_role)
        for question_data in questions:
            question = InterviewQuestion.objects.create(
                company=company,
                job_role=job_role,
                question_type=question_data['type'],
                question=question_data['question'],
                answer=question_data.get('answer', ''),
                difficulty_level=question_data.get('difficulty', 'medium')
            )
            SessionQuestion.objects.create(
                session=session,
                question=question
            )
        
        return redirect('ai_tools:interview_session', session_id=session.id)
    
    return render(request, 'ai_tools/interview_preparation.html', {
        'student_profile': student_profile,
        'companies': companies
    })

@login_required
def interview_session(request, session_id):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    session = get_object_or_404(InterviewSession, id=session_id, student=student_profile)
    
    if request.method == 'POST' and not session.is_completed:
        question_id = request.POST.get('question_id')
        answer = request.POST.get('answer')
        
        session_question = get_object_or_404(SessionQuestion, session=session, question_id=question_id)
        session_question.student_answer = answer
        session_question.is_answered = True
        session_question.save()
        
        # Check if all questions are answered
        unanswered_count = SessionQuestion.objects.filter(session=session, is_answered=False).count()
        if unanswered_count == 0:
            session.is_completed = True
            session.completed_at = timezone.now()
            session.save()
            messages.success(request, 'Interview session completed!')
    
    session_questions = SessionQuestion.objects.filter(session=session).order_by('id')
    current_question = session_questions.filter(is_answered=False).first()
    
    return render(request, 'ai_tools/interview_session.html', {
        'student_profile': student_profile,
        'session': session,
        'session_questions': session_questions,
        'current_question': current_question
    })

@login_required
def interview_history(request):
    if not request.user.is_student:
        return redirect('accounts:login')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('students:profile_complete')
    
    sessions = InterviewSession.objects.filter(student=student_profile).order_by('-started_at')
    
    return render(request, 'ai_tools/interview_history.html', {
        'student_profile': student_profile,
        'sessions': sessions
    })

def generate_resume_content(student_profile):
    """Generate AI-powered resume content based on student profile"""
    content = f"""
# {student_profile.full_name}

## Contact Information
- Email: {student_profile.user.email}
- Phone: {student_profile.user.phone or 'Not provided'}
- College: {student_profile.college_name}
- Branch: {student_profile.get_branch_display()}
- Graduation Year: {student_profile.graduation_year}

## Education
- **{student_profile.get_branch_display()}** - {student_profile.college_name} (Expected {student_profile.graduation_year})
- GPA: {student_profile.gpa or 'Not specified'}

## Skills
{student_profile.skills}

## About Me
{student_profile.about_me or 'Passionate and dedicated student seeking opportunities to apply academic knowledge in practical settings.'}

## Projects
*Note: Add your academic and personal projects here with descriptions and technologies used.*

## Experience
*Note: Add any internships, part-time jobs, or relevant work experience.*

## Online Profiles
- LinkedIn: {student_profile.linkedin_profile or 'Not provided'}
- GitHub: {student_profile.github_profile or 'Not provided'}
"""
    return content

def generate_interview_questions(company, job_role):
    """Generate AI-powered interview questions based on company and role"""
    questions = []
    
    # Technical questions
    if job_role.lower() in ['software engineer', 'developer', 'programmer']:
        questions.extend([
            {
                'type': 'technical',
                'question': 'Explain the difference between procedural programming and object-oriented programming.',
                'answer': 'Procedural programming focuses on procedures/functions that operate on data, while OOP organizes code around objects that contain both data and methods. OOP provides better encapsulation, inheritance, and polymorphism.',
                'difficulty': 'medium'
            },
            {
                'type': 'technical',
                'question': 'What is the time complexity of binary search and when would you use it?',
                'answer': 'Binary search has O(log n) time complexity. Use it when searching in sorted arrays or when you need efficient lookups in ordered data structures.',
                'difficulty': 'medium'
            }
        ])
    
    # HR questions
    questions.extend([
        {
            'type': 'hr',
            'question': 'Tell me about yourself.',
            'answer': 'Provide a brief introduction covering your background, education, key skills, and career goals.',
            'difficulty': 'easy'
        },
        {
            'type': 'hr',
            'question': 'Why do you want to work for our company?',
            'answer': 'Research the company and mention specific aspects like their products, culture, values, or opportunities that align with your career goals.',
            'difficulty': 'medium'
        }
    ])
    
    # Behavioral questions
    questions.extend([
        {
            'type': 'behavioral',
            'question': 'Describe a challenging situation you faced and how you overcame it.',
            'answer': 'Use the STAR method: Situation, Task, Action, Result. Be specific about the challenge, your actions, and the positive outcome.',
            'difficulty': 'medium'
        }
    ])
    
    return questions[:5]  # Return 5 questions for a session
