from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


# Create your models here.


class Banner(models.Model):
    """课程分类"""
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='banner/%Y%m', max_length=100)
    url = models.URLField('链接地址', max_length=200)
    is_show = models.BooleanField('是否首页显示', default=True)
    test_number = models.IntegerField('测试人数', default=0)
    push_time = models.DateTimeField('推送时间', default=datetime.now)

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = '课程分类'


class TestName(models.Model):
    """测评分类名称"""
    name = models.CharField('测试名称', max_length=20, verbose_name='测试名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='父级测试')

    class Meta:
        verbose_name = '测评分类名称'
        verbose_name_plural = '测评分类名称'

    def __str__(self):
        return self.name


class TestDetails(models.Model):
    """测试详情"""
    parent_test_name = models.ForeignKey(TestName, on_delete=models.PROTECT,
                                         related_name='parent_test_name', verbose_name='一级测试名称')
    child_test_name = models.ForeignKey(TestName, on_delete=models.PROTECT,
                                        related_name='child_test_name', verbose_name='二级测试名称')
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='banner/%Y%m', max_length=100)
    url = models.URLField('链接地址', max_length=200)
    is_index_show = models.BooleanField('是否首页显示', default=True)
    is_class_show = models.BooleanField('是否分类页显示', default=True)
    test_number = models.IntegerField('测试人数', default=0)
    test_dec = models.CharField('测试简介', max_length=100)
    push_time = models.DateTimeField('推送时间', default=datetime.now)

    class Meta:
        verbose_name = '测试详情'
        verbose_name_plural = '测试详情'


class TestIn(models.Model):
    """测试说明页"""
    introduce = models.CharField('介绍', max_length=500)
    theory = models.CharField('理论', max_length=500)
    notice = models.CharField('须知', max_length=500)

    class Meta:
        verbose_name = '测试说明页'
        verbose_name_plural = '测试说明页'
