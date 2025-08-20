# forms.py (updated)
from django import forms
from .models import ProjectInquiry


class ProjectInquiryForm(forms.ModelForm):
    """Form for project inquiries"""
    
    class Meta:
        model = ProjectInquiry
        fields = [
            'name', 'email', 'phone', 'service_type', 'budget_range', 
            'timeline', 'project_description', 'property_address'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-control'
            }),
            'service_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'budget_range': forms.Select(attrs={
                'class': 'form-control'
            }),
            'timeline': forms.TextInput(attrs={
                'placeholder': 'e.g., 3-6 months, ASAP, etc.',
                'class': 'form-control'
            }),
            'project_description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about your project requirements...',
                'class': 'form-control'
            }),
            'property_address': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Location of your property...',
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'


class QuickContactForm(forms.Form):
    """Quick contact form for project pages"""
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Name',
        'class': 'form-control'
    }))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Brief message about your inquiry...',
        'rows': 3,
        'class': 'form-control'
    }))