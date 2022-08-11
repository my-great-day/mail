from django.db import models
from datetime import datetime


# Create your models here.
class Users(models.Model):
    login = models.EmailField(verbose_name='Login')
    password = models.CharField(max_length=250, verbose_name='Password')
    create_account_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.login


class Code(models.Model):
    mail = models.EmailField()
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.mail
