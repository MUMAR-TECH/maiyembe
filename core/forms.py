from django import forms
from .models import ContactMessage, Service, ServiceFeature, Subscriber, ServiceRequest, TeamMember, Testimonial

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
    """Enhanced Form for service requests with budget information"""
    
    class Meta:
        model = ServiceRequest
        fields = [
            'service', 'name', 'email', 'phone', 'message', 
            'contact_method', 'budget_range', 'custom_budget',
            'project_location', 'project_timeline'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your project requirements, specific needs, and any special considerations...',
                'rows': 5,
                'required': True
            }),
            'contact_method': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'budget_range': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'custom_budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter specific budget amount',
                'step': '0.01',
                'min': '0'
            }),
            'project_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where is your project located?'
            }),
            'project_timeline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Desired timeline for completion'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].widget = forms.HiddenInput()
        self.fields['contact_method'].initial = 'whatsapp'
        self.fields['budget_range'].initial = 'custom'
        
        # Make custom_budget required only if budget_range is custom
        self.fields['custom_budget'].required = False

    def clean(self):
        cleaned_data = super().clean()
        budget_range = cleaned_data.get('budget_range')
        custom_budget = cleaned_data.get('custom_budget')
        
        if budget_range == 'custom' and not custom_budget:
            self.add_error('custom_budget', 'Please specify your budget amount when selecting custom budget.')
        
        return cleaned_data

class DirectBookingForm(forms.Form):
    """Simplified form for direct service booking"""
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'required': True
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone Number',
            'required': True
        })
    )
    contact_method = forms.ChoiceField(
        choices=ServiceRequest.CONTACT_METHODS,
        initial='whatsapp',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    project_location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Where is your project located?'
        })
    )
    project_timeline = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Desired timeline for completion'
        })
    )
    additional_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Any additional notes or requirements...',
            'rows': 3
        })
    )

class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'title', 'category', 'short_description', 'full_description', 
            'image', 'icon', 'is_featured', 'is_active', 'display_order',
            'starting_price', 'price_unit', 'price_description',
            'is_price_negotiable', 'price_display_type',
            'pricing_breakdown', 'estimated_duration',
            'includes_services', 'optional_addons'
        ]
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'full_description': forms.Textarea(attrs={'rows': 5}),
            'price_description': forms.Textarea(attrs={'rows': 3}),
            'starting_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'pricing_breakdown': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Enter each pricing detail on a new line'
            }),
            'includes_services': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'List each included service on a new line'
            }),
            'optional_addons': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'List each optional add-on with price on a new line'
            }),
        }

class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'title', 'category', 'short_description', 'full_description', 
            'image', 'icon', 'is_featured', 'is_active', 'display_order',
            'starting_price', 'price_unit', 'price_description',
            'is_price_negotiable', 'price_display_type',
            'pricing_breakdown', 'estimated_duration',
            'includes_services', 'optional_addons'
        ]
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'full_description': forms.Textarea(attrs={'rows': 5}),
            'price_description': forms.Textarea(attrs={'rows': 3}),
            'starting_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'pricing_breakdown': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Enter each pricing detail on a new line'
            }),
            'includes_services': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'List each included service on a new line'
            }),
            'optional_addons': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'List each optional add-on with price on a new line'
            }),
        }

class ServiceFeatureForm(forms.ModelForm):
    class Meta:
        model = ServiceFeature
        fields = ['title', 'description', 'icon']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }





class TestimonialForm(forms.ModelForm):
    """Form for testimonials"""
    class Meta:
        model = Testimonial
        fields = [
            'client_name', 'company', 'position', 'testimonial', 
            'image', 'rating', 'status', 'is_featured', 'order'
        ]
        widgets = {
            'testimonial': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_featured']:
                field.widget.attrs.update({'class': 'form-control'})

class TeamMemberForm(forms.ModelForm):
    """Form for team members"""
    class Meta:
        model = TeamMember
        fields = [
            'name', 'position', 'bio', 'image', 'email', 'phone',
            'linkedin_url', 'twitter_url', 'is_leadership', 'status', 'order'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_leadership']:
                field.widget.attrs.update({'class': 'form-control'})