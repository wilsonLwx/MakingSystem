from django.contrib import admin
from .models import PDFupload, PDF


# Register your models here.
class PDFAdmin(admin.ModelAdmin):
    """课程分类"""
    list_display = ['name']


class PDFuploadAdmin(admin.ModelAdmin):
    """PDF上传"""
    list_display = ['file', 'name']


admin.site.register(PDFupload, PDFuploadAdmin)

# admin.site.register(PDF, PDFAdmin)

admin.site.site_header = '管理后台'
admin.site.site_title = '大学生领导力潜质研究院'
