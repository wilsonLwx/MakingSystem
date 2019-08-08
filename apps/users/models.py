from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Users(AbstractUser):
    name = models.CharField(max_length=10)
    email = models.EmailField(max_length=20)
    token = models.CharField(max_length=30)
