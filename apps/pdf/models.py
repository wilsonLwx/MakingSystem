from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
from makingsystem.settings import base
# Create your models here.


class PDF(models.Model):
    """PDF"""
    from users.models import Users
    name = models.CharField("PDF名称", max_length=100)
    aliosspath = models.CharField("阿里云路径", max_length=100)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="PDF用户")


    class Meta:
        verbose_name = "PDF"
        verbose_name_plural = verbose_name


class PDFupload(models.Model):
    """PDF 上传"""
    file = models.FileField(upload_to=base.FILE_URL, verbose_name="文件选择")
    name = models.CharField(max_length=200, blank=True, verbose_name="文件名称")

    class Meta:
        unique_together = ('file', 'name')
        db_table = 'test_file'
        verbose_name = "文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

