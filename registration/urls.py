from django.urls import path, reverse_lazy
from .views import SignUpView, ActivateAccount, ProfileView, LoginView, AddcustomerView, CustomerView, deleteaddress
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('addcustomer/', AddcustomerView.as_view(), name='addcustomer'),
    path('customers/', CustomerView.as_view(), name='customers'),
    path('deleteaddress/<int:id>/', deleteaddress, name='deleteaddress'),

    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/change-password.html',
            success_url = '/'
        ),
        name='change-password'
    ),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password-reset/password-reset.html',
             subject_template_name='registration/password-reset/password-reset-subject.txt',
             email_template_name='registration/password-reset/password-reset-email.html',
             success_url='/password-reset/done/'
         ),
         name='password-reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password-reset/password-reset-done.html'
         ),
         name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password-reset/password-reset-confirm.html',
             success_url = reverse_lazy('password-reset-complete')
         ),
         name='password-reset-confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password-reset/password-reset-complete.html'
         ),
         name='password-reset-complete'),
]