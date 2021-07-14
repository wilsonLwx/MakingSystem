from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.


class SlideShow(models.Model):
    """轮播图"""
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='image/', max_length=100)
    push_time = models.DateTimeField('推送时间', default=datetime.now)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """课程分类"""
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('显示图', upload_to='image/', max_length=100)
    url = models.URLField('链接地址', max_length=200, default="www.baidu.com")
    is_show = models.BooleanField('是否首页显示', default=True)
    test_number = models.IntegerField('测试人数', default=0)
    push_time = models.DateTimeField('推送时间', default=datetime.now)

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = '课程分类'


class TestName(models.Model):
    """测评分类名称"""
    name = models.CharField(max_length=20, verbose_name='测试名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='父级测试')
    class Meta:
        verbose_name = '测评分类'
        verbose_name_plural = '测评分类'

    def __str__(self):
        return self.name


class TestDetails(models.Model):
    """测试详情"""
    parent_test_name = models.ForeignKey(TestName, on_delete=models.PROTECT,
                                         related_name='parent_test_name', verbose_name='一级测试名称')
    child_test_name = models.ForeignKey(TestName, on_delete=models.PROTECT,
                                        related_name='child_test_name', verbose_name='二级测试名称')
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('显示图', upload_to='image/', max_length=100)
    url = models.URLField('链接地址', max_length=200, default="www.baidu.com")
    is_index_show = models.BooleanField('是否首页显示', default=True)
    is_class_show = models.BooleanField('是否分类页显示', default=True)
    is_index_wheel_show = models.BooleanField('是否首页轮播显示显示', default=True)
    test_number = models.IntegerField('测试人数', default=0)
    test_dec = models.CharField('测试简介', max_length=100)
    push_time = models.DateTimeField('推送时间', default=datetime.now)

    class Meta:
        verbose_name = '测试详情'
        verbose_name_plural = '测试详情'


class TestIn(models.Model):
    """测试说明页"""
    title = models.CharField('标题', max_length=100)
    introduce = RichTextField('介绍')
    theory = RichTextField('理论', default="None")
    notice = RichTextField('须知', default="None")
    # introduce = models.CharField('介绍', max_length=500)
    # theory = models.CharField('理论', max_length=500)
    # notice = models.CharField('须知', max_length=500)

    class Meta:
        verbose_name = '测试说明'
        verbose_name_plural = '测试说明'


class AboutUs(models.Model):
    """关于我们"""
    about_us = RichTextField('关于我们')
   #  about_us = models.CharField('关于我们', max_length=500)
    class Meta:
        verbose_name = '关于我们'
        verbose_name_plural = '关于我们'
