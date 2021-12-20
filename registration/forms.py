from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

class SignUpForm(UserCreationForm):
 password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your Password', 'class':'input-box', 'required': True}))
 password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class':'input-box', 'required': True}))
 class Meta:
  model = User
  fields = ['username', 'email', 'password1', 'password2']
  widgets = {
      'username': forms.TextInput(attrs={'placeholder': 'Your Username', 'class': 'input-box', 'required': True}),
      'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'input-box', 'required': True}),
  }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'Your Username', 'class': 'input-box', 'required': True}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Your Password', 'class':'input-box', 'required': True}))
