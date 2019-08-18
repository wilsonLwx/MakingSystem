import os
import re

import oss2
import zipfile
from apps.users.models import Users
from apps.pdf.models import PDF
# 用户登录名称 object-oss@1463266644828335.onaliyun.com
# AccessKey ID LTAIeFNriSXX6ySq
# AccessKeySecret QHdxPWx7JU9q6Y55D3feQxlwcfZb66

import logging
from utils.log import log
log.initLogConf()

LOG = logging.getLogger(__file__)



class Xfer(object):

    def __init__(self, AccessKeyId, AccessKeySecret, Endpoint, bucketName):

        self.auth = None
        self.bucket = None
        self.AccessKeyId = AccessKeyId
        self.ACCessKeySecret = AccessKeySecret
        self.Endpoint = Endpoint
        self.bucketName = bucketName

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
        LOG.info(f'{"+"*10}uploading {"+"*10}')
        zfile = zipfile.ZipFile(localpath, 'r')
        for fileN in zfile.namelist():
            if fileN.endswith('/'):
                continue
            name = fileN.encode('cp437').decode('gbk')
            mobile = re.compile('1[345678]\d{9}')
            mobileNum = mobile.search(name)
            if not Users.objects.filter(mobile=mobileNum).first():
                LOG.error(f"用户不存在")
            PDFInfo = PDF()
            PDFInfo.name = name.split('/')[-1]
            PDFInfo.aliosspath = name
            PDFInfo.user = mobileNum
            PDFInfo.save()
            data = zfile.read(fileN)
            self.bucket.put_object(name, data)
        try:
            os.remove(localpath)
        except OSError as e:
            pass

