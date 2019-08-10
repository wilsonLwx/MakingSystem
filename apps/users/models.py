from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Users(AbstractUser):
    real_name = models.CharField(max_length=10)
    mobile = models.CharField(max_length=11)
    gender = models.BooleanField(default=False)
    email = models.EmailField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    token = models.CharField(max_length=30)
    profession = models.CharField(max_length=20)
    number = models.IntegerField()
    date_birth = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=10)
    education = models.CharField(max_length=10)
    vocation = models.CharField(max_length=20)

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return Users.real_name
