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


class ClassBanner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='banner/%Y%m', max_length=100)
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    is_show = models.BooleanField('是否显示', default=False)

    class Meta:
        verbose_name = '课程分类图'
        verbose_name_plural = verbose_name


class TestName(models.Model):
    """测试类名"""
    name = models.CharField('测评类名', max_length=100)

    class Meta:
        verbose_name = '测评类名'
        verbose_name_plural = verbose_name


class TestDetail(models.Model):
    """测试详情"""
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='banner/%Y%m', max_length=100)
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    is_index_show = models.BooleanField('首页是否显示', default=True)
    is_test_show = models.BooleanField('分类页是否显示', default=True)
    test_number = models.IntegerField('已测试人数', default=0)

    class Meta:
        verbose_name = '测试详情'
        verbose_name_plural = verbose_name


class TestInstruction(models.Model):
    """测试介绍页"""
    instruction = models.CharField('测评介绍', max_length=100)
    theory = models.CharField('测评理论', max_length=100)
    notice = models.CharField('测评须知', max_length=200)

    class Meta:
        verbose_name = '测试介绍'
        verbose_name_plural = verbose_name
