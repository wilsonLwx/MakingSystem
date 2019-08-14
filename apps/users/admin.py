from django.contrib import admin
from .models import Users, ClassBanner, Banner, LeaderBanner


# Register your models here.
<<<<<<< HEAD

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

=======
from .models import Banner, Users, ClassBanner


class BannerAdmin(admin.ModelAdmin):
    """评论轮播图"""
    list_display = ['id', 'title', 'url', 'index', 'add_time']


class UsersAdmin(admin.ModelAdmin):
    """用户"""
    list_display = ['id', 'username', 'real_name', 'email', 'mobile',
                    'gender', 'school', 'profession', 'education', 'vocation']


class ClassBannerAdmin(admin.ModelAdmin):
    """课程分类轮播图"""
    list_display = ['id', 'title', 'url', 'index', 'add_time']


admin.site.register(Banner, BannerAdmin)
admin.site.register(ClassBanner, ClassBannerAdmin)
admin.site.register(Users, UsersAdmin)

admin.site.site_header = '管理后台'
admin.site.site_title = '大学生领导力潜质研究院'
>>>>>>> b48fcee63e8af073648b37a9415508d1921e024a
