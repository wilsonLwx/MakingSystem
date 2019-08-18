from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Users(AbstractUser):
    # gender_choices = (
    #     ('male', '男'),
    #     ('female', '女')
    # )

    openid = models.CharField("用户唯一码", max_length=100, null=True)
    mobile = models.CharField("手机号", max_length=11)
    # gender = models.CharField("性别", max_length=20, choices=gender_choices, default='male')
    # email = models.EmailField("邮箱", max_length=20, blank=True, null=True)
    # school = models.CharField("学校", max_length=20, null=True)
    name = models.CharField("昵称", max_length=10, null=True)
    # profession = models.CharField("专业", max_length=20, null=True)
    # number = models.IntegerField("编号", null=True)
    # date_birth = models.DateField("生日", auto_now_add=True)
    # grade = models.CharField("年级", max_length=10, null=True)
    # education = models.CharField("学历", max_length=10, null=True)
    # vocation = models.CharField("意向行业", max_length=20, null=True)
    image = models.ImageField('用户头像', upload_to='image/%Y%m', default='image/default.png', max_length=100)

    class Meta:
        db_table = 'Users'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return Users.name


class CollectInfo(models.Model):
    """统计信息"""
    registration = models.IntegerField("注册量", default=0)
    upload_number = models.IntegerField("上传报告数量", default=0)
    read_number = models.IntegerField("阅读报告数量", default=0)

    class Meta:
        verbose_name = '数据统计'
        verbose_name_plural = verbose_name

