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
        # 后台统计数据
        get_info()
        return self.list_display

    list_display = ['registration', 'upload_number', 'read_number']


admin.site.register(Users, UsersAdmin)


admin.site.site_header = '管理后台'
admin.site.site_title = '大学生领导力潜质研究院'

class ClassBannerAdmin(admin.ModelAdmin):
    """课程分类admin后台管理"""
    list_display = ['title', 'image', 'url', 'index', 'add_time']


class BannerAdmin(admin.ModelAdmin):
    """首页轮播图admin后台管理"""
    list_display = ['title', 'image', 'url', 'index', 'add_time']


class LeaderBannerAdmin(admin.ModelAdmin):
    """领导分类图admin后台管理"""
    list_display = ['title', 'image', 'url', 'index', 'add_time']


admin.site.register(ClassBanner, ClassBannerAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(LeaderBanner, LeaderBannerAdmin)
admin.site.register(CollectInfo, CollectInfoAdmin)
