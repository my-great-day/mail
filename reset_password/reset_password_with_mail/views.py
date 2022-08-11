import random
from typing import Tuple, Any

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users, Code


# Create your views here.
@api_view(['POST'])
def index(request):
    if request.method == 'POST':
        _login = request.data.get('email_field')
        _password = request.data.get('password_field')
        if _login and _password and Users.objects.filter(login=_login, password=_password).first():
            return Response({'msg': 'Hello'})

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def send_reset_mail(request):
    _login = request.data.get('email_field')
    if _login and Users.objects.filter(login=_login).first():
        check_code(_login, func_send_reset_mail(_login))
        return Response({'msg': 'Hello!'})

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def confirm_mail(request):
    _mail = request.data.get('mail')
    _number = request.data.get('number_field')
    if check_code2(_mail, _number):
        return Response({'msg': 'Hello!'})

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def change_mail(request):
    _mail = request.data.get('mail')
    _password1 = request.data.get('password_field1')
    _password2 = request.data.get('password_field2')
    if _password1 == _password2 and _mail:
        user = Users.objects.filter(login=_mail).first()
        user.password = _password1
        user.save()
        return Response({'msg': 'Hello!'})

    return Response(status=status.HTTP_404_NOT_FOUND)


def func_send_reset_mail(login) -> int:
    _random_number = random.randint(100000, 999999)
    subject = 'Отправиль Wee компания'
    message = f'Ваш 6-значный код для потверждение: {_random_number}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [login, ]

    send_mail(subject, message, email_from, recipient_list)
    return _random_number


def check_code(mail, number):
    code = Code.objects.filter(mail=mail).first()
    if code:
        if code.code != number and code.mail == mail:
            code = Code.objects.filter(mail=mail).first()
            code.code = number
            code.save()
    else:
        code = Code(mail=mail, code=func_send_reset_mail(mail))
        code.save()


def check_code2(mail, number) -> bool:
    code = Code.objects.filter(mail=mail).first()
    if code.code == number and code.mail == mail:
        return True

    return False
