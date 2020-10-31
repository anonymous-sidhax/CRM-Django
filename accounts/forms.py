from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError # For validation of UserCreation Form



class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if email  == User.objects.filter(email=email)[0].email:
                raise ValidationError('Email already used')
            else:
                return email
        except IndexError:
            print(email)
            return email
            



class UserLogin(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
