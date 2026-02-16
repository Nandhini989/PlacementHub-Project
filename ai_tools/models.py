from django.db import models
from django.conf import settings

class Resume(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='ai_resumes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.title}"

class InterviewQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('hr', 'HR'),
        ('behavioral', 'Behavioral'),
        ('situational', 'Situational'),
    ]

    company = models.ForeignKey('companies.CompanyProfile', on_delete=models.CASCADE, related_name='interview_questions', blank=True, null=True)
    job_role = models.CharField(max_length=100, blank=True, null=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    difficulty_level = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        company_name = self.company.company_name if self.company else 'General'
        return f"{company_name} - {self.question_type} - {self.question[:50]}..."

class InterviewSession(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='interview_sessions')
    company = models.ForeignKey('companies.CompanyProfile', on_delete=models.CASCADE, blank=True, null=True)
    job_role = models.CharField(max_length=100, blank=True, null=True)
    questions = models.ManyToManyField(InterviewQuestion, through='SessionQuestion')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.full_name} - Interview Session"

class SessionQuestion(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    student_answer = models.TextField(blank=True, null=True)
    is_answered = models.BooleanField(default=False)
    answered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ['session', 'question']
