from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages # Django message framework
from django.contrib.auth.models import User # Default user model
from django.contrib.auth.decorators import login_required # Login required
from django.contrib.auth.forms import PasswordResetForm # For password reset
from django.http import HttpResponse 
from .forms import UserCreation, UserLogin
from django.contrib.auth.forms import PasswordResetForm # For for password reset
from django.db.models.query_utils import Q # For searching
from django.utils.http import urlsafe_base64_encode # For uuid
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator # Token Generator
from django.template.loader import render_to_string # Render to the string
from django.core.mail import send_mail, BadHeaderError # For Error handling with email bad header
from django.http import HttpResponse 

from django.core.mail import EmailMultiAlternatives # Email
from django import template # For loading html template in gmail




def login_request(request):
    if request.method == "POST":
            form = UserLogin(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username= username, password=password)
                if user is not None:
                    login(request, user)
                    redirection_url = request.POST.get('next')
                    if redirection_url:
                        print (redirection_url)
                        return HttpResponseRedirect(redirection_url)
                    else:
                        messages.success(request, f"Logged in successfully as {username}")
                        return redirect('home')
                else:
                    messages.error(request, "User Doesn't Exists.")
                    return render(request, "accounts/login.html", {'form':form})
    else:
        form = UserLogin()
    return render(request, "accounts/login.html", {'form':form})


def signup_request(request):
    form = UserCreation()
    if request.method == "POST":
        form = UserCreation(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email  = form.cleaned_data.get('email')
            User.objects.create_user(username=username, password=password, email=email)
            return redirect('accounts:login')

    return render(request, 'accounts/signup.html', {'form':form})



@login_required(login_url='accounts:login')
def logout_request(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect('home')




@login_required(login_url='accounts:login')
def password_reset_request(request):
    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            associated_users = User.objects.filter(Q(email=email)|Q(username=email))
            if associated_users.exists():
                for user in associated_users:
                    subject = 'Password Reset Requested'
                    plaintext = template.loader.get_template('registration/password/password_reset_email.txt')
                    htmltemp = template.loader.get_template('registration/password/password_reset_email.html')
                    c = {
                        'email':user.email,
                        'domain':'localhost:8000', # Update Needed
                        'site_name':'CRM-Django', # Update Needed
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':default_token_generator.make_token(user),
                        'protocol':'http', # Update Needed
                    }
                    template_content = htmltemp.render(c)
                    text_content = plaintext.render(c)
                    try:
                        msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email='aayushpatil558321@gmail.com', to=[user.email])
                        msg.attach_alternative(template_content, 'text/html')
                        msg.send()
                        
                    except BadHeaderError:
                        return HttpResponse('Invalid Header Found')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect('home')
            else:
                messages.error(request, 'An invalid email has been entered.')
    return render(request, "registration/password/password_reset.html", {'form':form})
