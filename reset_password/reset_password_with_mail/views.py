from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .check_bd import get_check_code, set_check_code, save_password
from .models import Users


@api_view(['POST', 'GET'])
def index(request):
    """Основной функция странице index"""
    if request.method == 'POST':
        _login = request.data.get('email_field')
        _password = request.data.get('password_field')
        if _login and _password and Users.objects.filter(login=_login, password=_password).first():
            return Response(status=status.HTTP_200_OK)

    return Response({'msg': 'Неверно введен логин или пароль!'}, status=status.HTTP_302_FOUND)


@api_view(['POST'])
def send_reset_mail(request):
    """Функция отправляет код с подверждениям"""
    _login = request.data.get('email_field')
    if _login and Users.objects.filter(login=_login).first():
        token = Token.generate_key()
        set_check_code(_login, token)
        return Response({'token': token}, status=status.HTTP_200_OK)

    return Response({'msg': 'Неверно введен логин!'}, status=status.HTTP_302_FOUND)


@api_view(['POST'])
def confirm_mail(request):
    """Функция потверждает отправленный код"""
    _mail = request.data.get('mail')
    _number = request.data.get('number_field')
    if get_check_code(_mail, _number):
        return Response(status=status.HTTP_200_OK)

    return Response({'msg': 'Неверно введен код!'}, status=status.HTTP_302_FOUND)


@api_view(['POST'])
def change_mail(request):
    """Функция изменяет пароль"""
    _mail = request.data.get('mail')
    _password1 = request.data.get('password_field1')
    _password2 = request.data.get('password_field2')
    if save_password(_password1, _password2, _mail):
        return Response(status=status.HTTP_200_OK)

    return Response({'msg': 'Пароль не совпадает\nПоля должнен быт одинаковым!!'}, status=status.HTTP_302_FOUND)


