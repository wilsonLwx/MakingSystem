import copy

from django.contrib import admin

# Register your models here.


from .models import Users, CollectInfo
from utils.get_collect_info import get_info


class UsersAdmin(admin.ModelAdmin):
    """用户管理后台"""
    list_display = ['id', 'username', 'mobile', 'is_superuser']


class CollectInfoAdmin(admin.ModelAdmin):
    """数据统计后台"""

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        # 后台统计数据
        get_info()
        return self.list_display

    list_display = ['registration', 'upload_number', 'read_number']


admin.site.register(Users, UsersAdmin)
admin.site.register(CollectInfo, CollectInfoAdmin)
