from django.urls import path
from registration.forms import SignUpForm, LoginForm
from .views import signup, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm, extra_context={'signupform': SignUpForm}), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
