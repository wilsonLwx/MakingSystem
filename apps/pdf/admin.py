from django.contrib import admin
from .models import PDFupload, PDF


# Register your models here.
class PDFAdmin(admin.ModelAdmin):
    """课程分类"""
    list_display = ['name']


class PDFuploadAdmin():
    """PDF上传"""
    list_display = ['file', 'name']


admin.site.register(PDFupload, PDFuploadAdmin)
