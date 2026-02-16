from django.db import models
from django.conf import settings

class CollegeProfile(models.Model):
    COLLEGE_TYPE_CHOICES = [
        ('GOVT', 'Government'),
        ('PRIVATE', 'Private'),
        ('AUTONOMOUS', 'Autonomous'),
        ('DEEMED', 'Deemed University'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='college_profile')
    college_name = models.CharField(max_length=200)
    college_email = models.EmailField()
    placement_officer_name = models.CharField(max_length=100)
    college_logo = models.ImageField(upload_to='college_logos/', blank=True, null=True)
    college_type = models.CharField(max_length=10, choices=COLLEGE_TYPE_CHOICES)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    established_year = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.college_name

    class Meta:
        verbose_name_plural = "College Profiles"
