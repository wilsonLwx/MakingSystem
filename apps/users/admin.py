from django.contrib import admin

# Register your models here.
from .models import Users


class UsersAdmin(admin.ModelAdmin):
    """用户管理后台"""
    list_display = ['id', 'username', 'gender', 'mobile', 'is_superuser']


admin.site.register(Users, UsersAdmin)
