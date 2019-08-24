# __author__ = 'ly'
# __date__ = '2019/08/23'
"""
获取统计信息
"""
from users.models import Users  # 注册人数
from pdf.models import PDF  # 上传报告数量


def get_info():
    registration = Users.objects.all().count()
    upload_number = PDF.objects.all().count()
    # read_number =
