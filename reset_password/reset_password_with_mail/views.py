from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render


# Create your views here.

def index(request):
    subject = 'From Wee company'
    message = 'Your 6-digital code: 123456'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['idibek200@yandex.com', ]
    send_mail(subject, message, email_from, recipient_list)

    return render(request, "template/index.html")

