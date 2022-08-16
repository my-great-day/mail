import random

from django.conf import settings
from django.core.mail import send_mail

from .models import Code, Users


def _func_send_reset_mail(login) -> int:
    _random_number = random.randint(100000, 999999)
    subject = 'Отправиль Wee компания'
    message = f'Ваш 6-значный код для потверждение: {_random_number}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [login, ]

    send_mail(subject, message, email_from, recipient_list)
    return _random_number


def set_check_code(mail, token):
    code = Code.objects.filter(mail=mail).first()
    random_number = _func_send_reset_mail(mail)
    if code:
        if code.code != random_number and code.mail == mail and token:
            code.code = random_number
            code.token = token
            code.save()
    else:
        code = Code(mail=mail, code=random_number, token=token)
        code.save()


def get_check_code(mail, number) -> bool:
    code = Code.objects.filter(token=mail).first()
    if code.code == number and code.token == mail:
        return True

    return False


def save_password(pass1, pass2, mail) -> bool:
    if pass1 == pass2 and mail:
        code = Code.objects.get(token=mail)
        user = Users.objects.get(login=code.mail)
        user.password = pass1
        user.save()
        return True
    return False
