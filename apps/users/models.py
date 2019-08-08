from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Users(AbstractUser):
    real_name = models.CharField(max_length=10)
    moblie = models.IntegerField(max_length=11)
    gender = models.BooleanField(default=0)
    email = models.EmailField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    token = models.CharField(max_length=30)
    profession = models.CharField(max_length=20)
    number = models.IntegerField(max_length=20)
    date_birth = models.DateField()
    grade = models.CharField(max_length=10)
    education = models.CharField(max_length=10)
    vocation = models.CharField(max_length=20)
