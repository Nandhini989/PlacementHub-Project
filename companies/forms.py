from django import forms
from .models import CompanyProfile

class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'hr_name', 'company_email', 'industry_type', 'company_logo', 'website', 'description', 'founded_year', 'company_size', 'headquarters']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'hr_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HR Name'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Company Email'}),
            'industry_type': forms.Select(attrs={'class': 'form-control'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Company Website'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Company Description'}),
            'founded_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Founded Year'}),
            'company_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Size (e.g., 1-50, 51-200, 201-500, 500+)'}),
            'headquarters': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Headquarters Location'}),
        }
