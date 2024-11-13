from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm
from main.models import Subscription


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        Subscription.objects.create(user=user, is_subscribed=False)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = f'accounts/email_confirmation/{uid}/{token}/'
        send_mail(
            'Подтвердите свой электронный адрес',
            'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:'
            f'http:///127.0.0.1:8000/{activation_url}',
            recipient_list=[user.email],
            fail_silently=False,
            from_email=None
        )
        return redirect('board')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('board')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def signup_confirmation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш аккаунт активирован!')
    else:
        messages.error(request, 'Ошибка!')

    return redirect('login')
