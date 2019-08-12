from datetime import datetime

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
    profession = models.CharField(max_length=20)
    number = models.IntegerField()
    date_birth = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=10)
    education = models.CharField(max_length=10)
    vocation = models.CharField(max_length=20)

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return Users.name


class Banner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='banner/%Y%m', max_length=100)
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name


class ClassBanner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='banner/%Y%m', max_length=100)
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程分类图'
        verbose_name_plural = verbose_name


class LeaderBanner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='banner/%Y%m', max_length=100)
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '领导分类图'
        verbose_name_plural = verbose_name
