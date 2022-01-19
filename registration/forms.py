from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import Customer


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

# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'email',
            ]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'city', 'address', 'locality', 'phone_no','house_no', 'zip_code',]
        labels = {'house_no':'House no (Optional)','zip_code':'Zip code (Optional)'}
        widgets = {
            'house_no': forms.NumberInput(attrs={'required':False}),
            'zip_code':forms.NumberInput(attrs={'required':False}),
            }