from django.test import TestCase

# Create your tests here.
from django.core.cache import cache, caches

from makingsystem.settings.config import appid, appkey, signid

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
ssender = SmsSingleSender(appid, appkey)
params = ["5678"]  # 当模板没有参数时，`params = []`
phone_numbers = [13205827585, 17521125085]
sms_type = 0
try:
  # result = ssender.send_with_param(86, phone_numbers[0],
  #      params, sign=signid, extend="", ext="")
  result = ssender.send(sms_type, 86, phone_numbers[0],
               "【腾讯云】您的验证码是: 5678", extend="", ext="")
except HTTPError as e:
  print(e)
except Exception as e:
  print(e)
print(result)


