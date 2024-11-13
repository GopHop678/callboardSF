from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from django.core.mail import send_mail, EmailMultiAlternatives


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class LogInForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )


# class NewAdventurerForm(forms.Form):
#     username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "email",
#             "password1",
#             "password2",
#         )
