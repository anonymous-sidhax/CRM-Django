from .views import login_request, signup_request
from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('login/', login_request, name="login"),
    path('signup/', signup_request, name="signup"),
]
