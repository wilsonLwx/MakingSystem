from django.contrib import admin
from .models import Users, ClassBanner, Banner, LeaderBanner


# Register your models here.

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

