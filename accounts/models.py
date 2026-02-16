from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('company', 'Company'),
        ('college', 'College'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_company(self):
        return self.role == 'company'

    @property
    def is_college(self):
        return self.role == 'college'
