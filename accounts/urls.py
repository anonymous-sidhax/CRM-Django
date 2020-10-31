from .views import login_request, signup_request, logout_request, password_reset_request
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.shortcuts import HttpResponseRedirect


app_name = 'accounts'

urlpatterns = [
    path('login/', login_request, name="login"),
    path('signup/', signup_request, name="signup"),
    path("password-reset/", password_reset_request, name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html", success_url= reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'), 
    
]
