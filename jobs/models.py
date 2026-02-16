from django.db import models
from django.conf import settings

class JobPost(models.Model):
    JOB_TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    ]

    company = models.ForeignKey('companies.CompanyProfile', on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    skills_required = models.TextField(help_text="Enter required skills separated by commas")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    experience_required = models.IntegerField(default=0, help_text="Years of experience required")
    application_deadline = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"

    @property
    def application_count(self):
        return self.applications.count()

class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.job.title}"

    class Meta:
        unique_together = ['job', 'student']
        ordering = ['-applied_at']
