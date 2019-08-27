import os
import re

import oss2
import zipfile

from category.models import TestDetails, Banner
from pdf.models import PDF
from users.models import Users
from makingsystem.settings import config, MEDIA_ROOT
# 用户登录名称 object-oss@1463266644828335.onaliyun.com
# AccessKey ID LTAIeFNriSXX6ySq
# AccessKeySecret QHdxPWx7JU9q6Y55D3feQxlwcfZb66
from django.db import connection
import logging
from utils.log import log

from django.contrib import admin

log.initLogConf()

LOG = logging.getLogger(__file__)


class Xfer(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            obj = super().__new__(cls)
            # obj.rest = REST(serverIP, serverPort, softVersion)
            # obj.rest.setAccount(accountSid, accountToken)
            # obj.rest.setAppId(appId)

            cls.instance = obj
        return cls.instance

    def __init__(self):

        self.auth = None
        self.bucket = None
        self.AccessKeyId = config.AccessKeyId
        self.ACCessKeySecret = config.AccessKeySecret
        self.Endpoint = config.Endpoint
        self.bucketName = config.bucketName

    def initAliyun(self):
        if self.auth is None:
            self.auth = oss2.Auth(self.AccessKeyId, self.ACCessKeySecret)
            self.bucket = oss2.Bucket(self.auth, self.Endpoint, self.bucketName)

    def clearAliyun(self):
        self.auth = None
        self.bucket = None

    def upload(self, localpath):
        if not os.path.isfile(localpath):
            return
        LOG.info(f'{"+" * 10}uploading {"+" * 10}')
        zfile = zipfile.ZipFile(localpath, 'r')
        for fileN in zfile.namelist():
            if fileN.endswith('/'):
                continue
            # name = fileN.encode('cp437').decode('gbk')

            name = fileN
            mobile = re.compile('1[345678]\d{9}')
            mobileNum = mobile.search(name).group()
            PDFname = name.split('/')[-1]
            title_name = PDFname.split('+')[0]

            if PDF.objects.filter(name=PDFname).first():
                continue

            userInfo = Users.objects.filter(mobile=mobileNum).first()
            if not userInfo:
                LOG.info("用户未保存")
                userInfo = Users()
                userInfo.mobile = mobileNum
                userInfo.username = mobileNum
                userInfo.save()
            test_obj = TestDetails.objects.filter(title=title_name).first()
            banner_obj = Banner.objects.filter(title=title_name).first()
            print(title_name, test_obj)

            if test_obj:
                test_obj.test_number += 1
                test_obj.save()
            elif banner_obj:
                banner_obj.test_number += 1
                banner_obj.save()


            PDFInfo = PDF()
            PDFInfo.name = PDFname
            PDFInfo.aliosspath = name
            LOG.info(f'### mobileNum:{mobileNum}')
            PDFInfo.user = userInfo
            PDFInfo.save()
            data = zfile.read(fileN)
            self.bucket.put_object(name, data)
        try:
            os.remove(localpath)
        except OSError as e:
            pass

    def imageupload(self, name, image_path):
        LOG.info(f'{"+" * 10}uploading {"+" * 10}')
        self.bucket.put_object_from_file(name, image_path)

    def videoupload(self, name, video_path):
        LOG.info("上传video")
        self.bucket.put_object_from_file(name, video_path)

    def sign_url(self, name):
        url = self.bucket.sign_url('GET', name, 60 * 30).replace('http://', 'https://')
        return url


class uploadzipadmin(admin.ModelAdmin):
    """
    自动上传新建对象的文件至阿里云
    """

    def save_model(self, request, obj, form, change):
        obj.save()
        # LOG.info('----- 开始上传 下载 至本地: %s' % obj.image)
        zip_path = os.path.join(MEDIA_ROOT, obj.file.name)
        xfer = Xfer()
        xfer.initAliyun()
        xfer.upload(zip_path)
        xfer.clearAliyun()

        # print("@"*40)
        # print(obj.__dir__())
        # print("#"*50)
        # print(request.__dir__())
        # print(obj.name())
        try:
            os.remove(zip_path)
        except:
            pass


class UploadImageAdmin(admin.ModelAdmin):
    """
    自动上传新建对象的图片至阿里云
    """

    def save_model(self, request, obj, form, change):
        obj.save()
        LOG.info('----- 开始上传测试图片至阿里云: %s' % obj.image.name)
        image_path = os.path.join(MEDIA_ROOT, obj.image.name)
        xfer = Xfer()
        xfer.initAliyun()
        xfer.imageupload(obj.image.name, image_path)
        xfer.clearAliyun()


class UploadVdeioAdmin(admin.ModelAdmin):
    """
    上传Vedio到
    """
    def save_model(self, request, obj, form, change):
        obj.save()
        vedio_path = os.path.join(MEDIA_ROOT, obj.file.name)
        xfer = Xfer()
        xfer.initAliyun()
        xfer.videoupload(obj.file.name, vedio_path)
        xfer.clearAliyun()
        try:
            os.remove(vedio_path)
        except:
            pass


if __name__ == '__main__':
    x = Xfer()
    x.initAliyun()
    # url = x.sign_url("VIDEO/微信_2019-08-27_21-03-36_CeLuCuX.mp4")
    url = x.sign_url("VIDEO/微信_2019-08-27_21-03-36_CeLuCuX.mp4")
    print(url)
