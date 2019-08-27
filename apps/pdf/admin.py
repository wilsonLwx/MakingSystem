from django.contrib import admin
from .models import PDFupload, PDF, Videoupload

from utils.uploadaliyun import uploadzipadmin, UploadVdeioAdmin


# Register your models here.
class PDFAdmin(admin.ModelAdmin):
    """课程分类"""
    list_display = ['name']


class PDFuploadAdmin(uploadzipadmin):
    """PDF上传"""
    list_display = ['file', 'name']

class VdeiouploadAdmin(UploadVdeioAdmin):
    """VEDIO 上传"""
    list_display = ['file', 'name']


admin.site.register(PDFupload, PDFuploadAdmin)
# admin.site.register(Videoupload, VdeiouploadAdmin)