from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages # Django message framework
from django.contrib.auth.models import User # Default user model
from django.contrib.auth.decorators import login_required # Login required
from django.contrib.auth.forms import PasswordResetForm # For password reset
from django.http import HttpResponse 
from .forms import UserCreation, UserLogin





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

