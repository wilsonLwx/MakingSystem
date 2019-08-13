from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Users(AbstractUser):
    gender_choices = (
        ('male', '男'),
        ('female', '女')
    )

    real_name = models.CharField("真实姓名", max_length=10, null=True)
    mobile = models.CharField("手机号", max_length=11)
    gender = models.BooleanField("性别", choices=gender_choices, default="male")
    email = models.EmailField("邮箱", max_length=20, blank=True, null=True)
    school = models.CharField("学校", max_length=20, null=True)
    name = models.CharField("昵称", max_length=10)
    profession = models.CharField("专业", max_length=20, null=True)
    number = models.IntegerField("编号", null=True)
    date_birth = models.DateField("生日", auto_now_add=True)
    grade = models.CharField("年级", max_length=10, null=True)
    education = models.CharField("学历", max_length=10, null=True)
    vocation = models.CharField("意向行业", max_length=20, null=True)

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
        verbose_name_plural = '评估轮播图'


class ClassBanner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='classbanner/%Y%m', max_length=100)
    # url = models.URLField('访问地址', max_length=200, default='https://www.baidu.com/')
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '课程分类轮播图'
