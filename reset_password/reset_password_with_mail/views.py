import random

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from .models import Users


# Create your views here.

def index(request):
    msg = ''
    if request.POST:
        _login = request.POST.get('email_field')
        _password = request.POST.get('password_field')
        if _login and _password and Users.objects.filter(login=_login, password=_password).first():
            return redirect('sayHello/')

        msg = 'Неверно введен логин или пароль'
    return render(request, 'template/index.html', {'msg': msg})


def send_reset_mail(request):
    msg = ''
    if request.POST:
        _login = request.POST.get('email_field')
        if _login and Users.objects.filter(login=_login).first():
            request.session['rpwe'] = func_send_reset_mail(_login)
            return redirect(f'confirm/{_login}')

    return render(request, 'template/reset_password.html')


def confirm_mail(request, login):
    _save_random_in_session = int(request.session.get('rpwe'))
    if _save_random_in_session and request.POST:
        _number = int(request.POST.get('number_field'))
        if _save_random_in_session == _number:
            request.session['rpwe'] = login
            return redirect(reverse(change_mail))

    return render(request, 'template/confirm_mail.html')


def change_mail(request):
    msg = ''
    _save_random_in_session = request.session.get('rpwe')
    if _save_random_in_session and request.POST:
        password1 = request.POST.get('password_field1')
        password2 = request.POST.get('password_field2')
        if password1 == password2:
            user = Users.objects.filter(login=_save_random_in_session).first()
            user.password = password1
            user.save()
            return redirect(reverse(sayHello))

        msg = 'Проверте все поля!'
    return render(request, 'template/change_mail.html', {'msg': msg})


def func_send_reset_mail(login) -> int:
    _random_number = random.randint(100000, 999999)
    subject = 'Отправиль Wee компания'
    message = f'Ваш 6-значный код для потверждение: {_random_number}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [login, ]

    send_mail(subject, message, email_from, recipient_list)
    return _random_number


def sayHello(request):
    return HttpResponse('Hello!')
