from django import forms
from .models import ContactMessage, Service, ServiceFeature, Subscriber, ServiceRequest

class ContactForm(forms.ModelForm):
    """Form for contact messages"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'required': True,
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email',
                'required': True,
                'class': 'form-control'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your Message',
                'required': True,
                'class': 'form-control',
                'rows': 5
            })
        }

class SubscriberForm(forms.ModelForm):
    """Form for newsletter subscribers"""
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email Address',
                'required': True,
                'class': 'form-control'
            })
        }

class ServiceRequestForm(forms.ModelForm):
    """Form for service requests with WhatsApp integration"""
    class Meta:
        model = ServiceRequest
        fields = ['service', 'name', 'email', 'phone', 'message', 'contact_method']
        widgets = {
            'service': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Full Name',
                'required': True,
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email',
                'required': True,
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Your Phone Number',
                'required': True,
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project...',
                'required': True,
                'class': 'form-control',
                'rows': 5
            }),
            'contact_method': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set WhatsApp as default contact method
        self.fields['contact_method'].initial = 'whatsapp'


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'title', 'category', 'short_description', 'full_description', 
            'image', 'icon', 'is_featured', 'is_active'
        ]
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'full_description': forms.Textarea(attrs={'rows': 5}),
        }

class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'title', 'category', 'short_description', 'full_description', 
            'image', 'icon', 'is_featured', 'is_active', 'display_order'
        ]
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'full_description': forms.Textarea(attrs={'rows': 5}),
        }

class ServiceFeatureForm(forms.ModelForm):
    class Meta:
        model = ServiceFeature
        fields = ['title', 'description', 'icon']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }