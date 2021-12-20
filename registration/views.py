from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Signup View Function
def signup(request):
 if request.method == "POST":
  fm = SignUpForm(request.POST)
  loginform = LoginForm(request=request, data=request.POST)
  if fm.is_valid():
   messages.success(request, 'Account Created Successfully !!') 
   fm.save()
   return redirect('login')
 else: 
  fm = SignUpForm()
  loginform = LoginForm()
 return render(request, 'registration/signup.html', {'form':fm, 'loginform': loginform})

# Profile
def profile(request):
  if request.user.is_authenticated:
    return render(request, 'registration/profile.html', {'name': request.user})
  else:
    return redirect('login')