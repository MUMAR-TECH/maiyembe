# blog/forms.py
from django import forms
from .models import Category, Post, Comment, NewsletterSubscriber

class CategoryForm(forms.ModelForm):
    """Form for blog categories"""
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class PostForm(forms.ModelForm):
    """Form for blog posts"""
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'featured_image', 'excerpt', 'category', 
            'tags', 'status', 'published_date', 'meta_title', 'meta_description',
            'is_featured', 'is_pinned'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_featured', 'is_pinned']:
                field.widget.attrs.update({'class': 'form-control'})

class CommentForm(forms.ModelForm):
    """Form for blog comments (admin)"""
    class Meta:
        model = Comment
        fields = ['content', 'is_approved']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscribers"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name (optional)'}),
        }