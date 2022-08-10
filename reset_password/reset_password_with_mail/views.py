import random

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse


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
            save_random_in_session = request.session['rpwe'] = func_send_reset_mail()
            return redirect('confirm/', login=_login)

    return render(request, 'template/reset_password.html')


def func_send_reset_mail() -> int:
    _random_number = random.randint(100000, 999999)
    subject = 'Отправиль Wee компания'
    message = f'Ваш 6-значный код для потверждение: {_random_number}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['idibek200@yandex.com', ]

    send_mail(subject, message, email_from, recipient_list)
    return _random_number


def sayHello(request):
    return HttpResponse('Hello!')


def confirm_mail(request, login):
    msg = ''
    _save_random_in_session = int(request.session.get('rpwe'))
    if _save_random_in_session and request.POST:
        _number = int(request.POST.get('number_field'))

        if _save_random_in_session == _number:
            return redirect('change/')
        else:
            msg = 'Incorrect!'
            print(_number, _save_random_in_session, msg)

        return render(request, 'template/confirm_mail.html', {'msg': msg})


def change_mail(request):
    return render(request, 'template/change_mail.html')
