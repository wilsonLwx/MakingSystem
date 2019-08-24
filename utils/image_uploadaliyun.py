# import os
# import re

import oss2
# import zipfile

# from pdf.models import PDF
# from users.models import Users
from makingsystem.settings import config
# 用户登录名称 object-oss@1463266644828335.onaliyun.com
# AccessKey ID LTAIeFNriSXX6ySq
# AccessKeySecret QHdxPWx7JU9q6Y55D3feQxlwcfZb66
# from django.db import connection
import logging
from utils.log import log

log.initLogConf()

LOG = logging.getLogger(__file__)


# cursor = connection.cursor()


class Xfer(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            obj = super().__new__(cls)

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

    def upload(self, name, image_path):
        LOG.info(f'{"+" * 10}uploading {"+" * 10}')
        self.bucket.put_object_from_file(name, image_path)

    def sign_url(self, name):
        url = self.bucket.sign_url('GET', name, 60 * 30)
        return url


if __name__ == '__main__':
    x = Xfer()
    x.initAliyun()
    # url = x.sign_url("testPDF/123456.pdf")
    x.upload("test1url", "/home/ly/MakingSystem/media/image/5_9pkxn9R.jpg")
    url = x.sign_url("test1url")
    print(url)