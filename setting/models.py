from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from user.models import User
# Create your models here.

class Time_settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hour = models.CharField(max_length=2)
    min = models.CharField(max_length=2)
    ampm = models.CharField(max_length=2)
    date = models.TextField()
    onoff = models.BooleanField(default=True)


    # def __str__(self):
    #     return self.title

class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(null=True, default='', decimal_places=0, max_digits=12)
    deduction = models.DecimalField(null=True, default='', decimal_places=0, max_digits=12)

    # def __str__(self):
    #     return self.user

