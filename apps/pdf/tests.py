from django.test import TestCase

# Create your tests here.

import oss2
# 用户登录名称 object-oss@1463266644828335.onaliyun.com
# AccessKey ID LTAIeFNriSXX6ySq
# AccessKeySecret QHdxPWx7JU9q6Y55D3feQxlwcfZb66
auth = oss2.Auth('LTAIeFNriSXX6ySq', 'QHdxPWx7JU9q6Y55D3feQxlwcfZb66')

file_name = '/home/hw/test.pdf'

bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'hwihome')

# result = bucket.put_object_from_file('home/hw/test.pdf', file_name)


# if result.status == 200:
#     url = f'{file_name}'
#     print(url)
#
# print(result.status)


# from itertools import islice
#
# for b in islice(oss2.ObjectIterator(bucket), 10):
#     print(b.key)
#     print(b.__dir__())
#     print(b.last_modified)
#     print(b.etag)
#     print(b.storage_class)

pdf_url = bucket.sign_url('GET', 'home/hw/test.pdf', 200)

print(pdf_url)
