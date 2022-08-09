from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render


# Create your views here.

def index(request):
    if False:
        subject = 'welcome to GFG world'
        message = 'Hi thank you for registering.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['idibek200@yandex.com', ]
        send_mail(subject, message, email_from, recipient_list)

    return render(request, "template/index.html")

