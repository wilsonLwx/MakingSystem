from django.contrib import admin
from .models import Banner, TestDetails, TestIn, TestName


# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    """课程分类"""
    list_display = ['title', 'url', 'image', 'is_show', 'push_time']


class TestDetailsAdmin(admin.ModelAdmin):
    """测试详情"""
    list_display = ['title', 'parent_test_name', 'child_test_name', 'image', 'url', 'test_number',
                    'is_index_show', 'is_class_show', 'push_time', ]


class TestNameAdmin(admin.ModelAdmin):
    """测试分类名"""
    list_display = ['name', 'parent']


class TestInAdmin(admin.ModelAdmin):
    """分类页测试介绍"""
    list_display = ['introduce', 'theory', 'notice', 'detail']


admin.site.register(Banner, BannerAdmin)
admin.site.register(TestDetails, TestDetailsAdmin)
admin.site.register(TestName, TestNameAdmin)
admin.site.register(TestIn, TestInAdmin)

admin.site.site_header = '管理后台'
admin.site.site_title = '大学生领导力潜质研究院'
