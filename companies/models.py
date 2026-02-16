from django.db import models
from django.conf import settings

class CompanyProfile(models.Model):
    INDUSTRY_CHOICES = [
        ('IT', 'Information Technology'),
        ('FINANCE', 'Finance & Banking'),
        ('HEALTHCARE', 'Healthcare'),
        ('EDUCATION', 'Education'),
        ('MANUFACTURING', 'Manufacturing'),
        ('RETAIL', 'Retail & E-commerce'),
        ('CONSULTING', 'Consulting'),
        ('STARTUP', 'Startup'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200)
    hr_name = models.CharField(max_length=100)
    company_email = models.EmailField()
    industry_type = models.CharField(max_length=20, choices=INDUSTRY_CHOICES)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 1-50, 51-200, 201-500, 500+")
    headquarters = models.CharField(max_length=200, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "Company Profiles"
