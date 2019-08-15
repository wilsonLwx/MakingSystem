from django.contrib import admin

# Register your models here.
from .models import Users, CollectInfo


class UsersAdmin(admin.ModelAdmin):
    """用户管理后台"""
    list_display = ['id', 'username', 'gender', 'mobile', 'is_superuser']


class CollectInfoAdmin(admin.ModelAdmin):
    """数据统计后台"""
    list_display = ['registration', 'upload_number', 'read_number']


admin.site.register(Users, UsersAdmin)
admin.site.register(CollectInfo, CollectInfoAdmin)
