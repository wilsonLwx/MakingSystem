# encoding:utf-8
from django.test import TestCase

# Create your tests here.
import oss2

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
#
# pdf_url = bucket.sign_url('GET', 'home/hw/test.pdf', 200)
#
# print(pdf_url)


import zipfile

zfile = zipfile.ZipFile("/home/hw/MakingSystem/media/PDF/testPDF.zip", 'r')

for fileN in zfile.namelist():
    if fileN.endswith('/'):
        continue
    print(fileN.encode('cp437').decode('gbk'))
    name = fileN.encode('cp437').decode('gbk')
    data = zfile.read(fileN)
    # bucket.put_object(name, data)
    url = bucket.sign_url('GET', name, 200)
    print(url)
