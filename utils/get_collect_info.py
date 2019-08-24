# __author__ = 'ly'
# __date__ = '2019/08/23'
"""
获取统计信息
"""
from users.models import Users, CollectInfo  # 注册人数
from pdf.models import PDF  # 上传报告数量


def get_info():
    registration = Users.objects.all().count()
    upload_number = PDF.objects.all().count()
    info = CollectInfo()
    info.registration = int(registration) + 1
    info.read_number = int(registration) + 1
    info.upload_number = int(registration) + 1
    info.save()
