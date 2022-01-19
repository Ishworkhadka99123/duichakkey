from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'message']
        labels = {'full_name': 'Your Name', 'email': 'Your Email', 'message': 'Your Message'}