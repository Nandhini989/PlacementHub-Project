from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('IT', 'Information Technology'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    graduation_year = models.IntegerField()
    skills = models.TextField(help_text="Enter your skills separated by commas")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.college_name}"

    class Meta:
        verbose_name_plural = "Student Profiles"
