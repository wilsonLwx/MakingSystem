from django.contrib import admin

# Register your models here.
from .models import Users, CollectInfo


class UsersAdmin(admin.ModelAdmin):
    """用户管理后台"""
    list_display = ['id', 'username', 'mobile', 'is_superuser']


class CollectInfoAdmin(admin.ModelAdmin):
    """数据统计后台"""

    def get_inline_instances(self, request, obj=None):
        # 后台统计数据

        #  后台显示数据
        inline_instances = []
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                inline_has_add_permission = inline._has_add_permission(request, obj)
                if not (inline.has_view_or_change_permission(request, obj) or
                        inline_has_add_permission or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline_has_add_permission:
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances

    list_display = ['registration', 'upload_number', 'read_number']


admin.site.register(Users, UsersAdmin)
admin.site.register(CollectInfo, CollectInfoAdmin)
