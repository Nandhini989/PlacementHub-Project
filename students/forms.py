from django import forms
from .models import StudentProfile

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'college_name', 'branch', 'graduation_year', 'skills', 'resume', 'profile_image', 'gpa', 'about_me', 'linkedin_profile', 'github_profile']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'College Name'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Graduation Year'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Skills (comma separated)'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'GPA'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'About Me'}),
            'linkedin_profile': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn Profile URL'}),
            'github_profile': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub Profile URL'}),
        }
