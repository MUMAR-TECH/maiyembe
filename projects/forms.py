# forms.py (updated)
from django import forms
from .models import Project, ProjectCategory, ProjectImage, ProjectVideo, ProjectFeature, ProjectTestimonial, ProjectInquiry


class ProjectForm(forms.ModelForm):
    """Form for creating and updating projects"""
    categories = forms.ModelMultipleChoiceField(
        queryset=ProjectCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'client', 'location', 'completion_date',
            'project_duration', 'budget', 'size', 'featured_image', 'is_featured',
            'status', 'categories', 'meta_title', 'meta_description'
        ]
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['categories', 'is_featured']:
                field.widget.attrs.update({'class': 'form-control'})


class ProjectImageForm(forms.ModelForm):
    """Form for project images"""
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption', 'is_primary', 'is_landscape', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Image caption...'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProjectVideoForm(forms.ModelForm):
    """Form for project videos"""
    class Meta:
        model = ProjectVideo
        fields = ['video_url', 'caption', 'order']
        widgets = {
            'video_url': forms.URLInput(attrs={'placeholder': 'YouTube or Vimeo URL'}),
            'caption': forms.TextInput(attrs={'placeholder': 'Video caption...'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProjectFeatureForm(forms.ModelForm):
    """Form for project features"""
    class Meta:
        model = ProjectFeature
        fields = ['title', 'description', 'icon', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Feature description...'}),
            'icon': forms.TextInput(attrs={'placeholder': 'fas fa-home'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProjectTestimonialForm(forms.ModelForm):
    """Form for project testimonials"""
    class Meta:
        model = ProjectTestimonial
        fields = ['client_name', 'client_position', 'testimonial', 'avatar', 'rating', 'is_featured']
        widgets = {
            'testimonial': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Client testimonial...'}),
            'client_position': forms.TextInput(attrs={'placeholder': 'Client position or company...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_featured']:
                field.widget.attrs.update({'class': 'form-control'})


class ProjectCategoryForm(forms.ModelForm):
    """Form for project categories"""
    class Meta:
        model = ProjectCategory
        fields = ['name', 'description', 'image', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})




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