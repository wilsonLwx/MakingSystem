from django.contrib import admin
from .models import PDFupload


# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    """课程分类"""
    list_display = ['title', 'url', 'image', 'is_show', 'push_time']


class PDFuploadAdmin(admin.ModelAdmin):
    """PDF上传"""
    list_display = ['file', 'name']


admin.site.site_header = '管理后台'
admin.site.site_title = '大学生领导力潜质研究院'
