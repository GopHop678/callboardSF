from django.urls import path
from .views import SignUp, user_login, user_logout, signup_confirmation

urlpatterns = [
    path('accounts/signup/', SignUp.as_view(), name='signup'),
    path('accounts/login', user_login, name='login'),
    path('accounts/logout', user_logout, name='logout'),
    path('accounts/email_confirmation/<uidb64>/<token>/', signup_confirmation, name='email_confirmation'),
]
