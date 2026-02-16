from django import forms
from .models import CollegeProfile

class CollegeRegistrationForm(forms.ModelForm):
    class Meta:
        model = CollegeProfile
        fields = ['college_name', 'college_email', 'placement_officer_name', 'college_logo', 'college_type', 'website', 'description', 'established_year', 'address', 'city', 'state', 'pincode', 'phone']
        widgets = {
            'college_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'College Name'}),
            'college_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'College Email'}),
            'placement_officer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placement Officer Name'}),
            'college_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'college_type': forms.Select(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'College Website'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'College Description'}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Established Year'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }
