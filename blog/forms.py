from django import forms
from core.models import Subscriber

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']