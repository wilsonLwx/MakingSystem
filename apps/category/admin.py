import os

from django.contrib import admin

from makingsystem.settings import MEDIA_ROOT
from .models import Banner, TestDetails, TestIn, TestName
from utils.image_uploadaliyun import Xfer


# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    """课程分类"""
    list_display = ['title', 'image', 'is_show', 'push_time']


class TestDetailsAdmin(admin.ModelAdmin):
    """测试详情"""

    def save_model(self, request, obj, form, change):
        print('---保存了图片--- %s' % obj.image)
        obj.save()
        print('----- 开始上传图片至阿里云: %s' % obj.image)
        image_path = os.path.join(MEDIA_ROOT, str(obj.image))
        xfer = Xfer()
        xfer.initAliyun()
        print('### form:', form)
        print('###  image_path', image_path)
        print('request--------->', request)
        # xfer.upload(str(obj.image), image_path)
        # xfer.upload(obj.image, request)
        # xfer.upload(str(obj.image), obj.image)

        # xfer.clearAliyun()

        # print('--------从阿里云获取url:-----------')
        # url = xfer.sign_url(str(obj.image))
        # print('----阿里云 url:', url)

    list_display = ['title', 'parent_test_name', 'child_test_name', 'image', 'test_number',
                    'is_index_show', 'is_class_show', 'push_time', ]


class TestNameAdmin(admin.ModelAdmin):
    """测试分类名"""
    list_display = ['name', 'parent', 'is_index_show']


class TestInAdmin(admin.ModelAdmin):
    """分类页测试介绍"""
    list_display = ['introduce', 'theory', 'notice']


admin.site.register(Banner, BannerAdmin)
admin.site.register(TestDetails, TestDetailsAdmin)
admin.site.register(TestName, TestNameAdmin)
admin.site.register(TestIn, TestInAdmin)

admin.site.site_header = '管理后台'
admin.site.site_title = '大学生领导力潜质研究院'
