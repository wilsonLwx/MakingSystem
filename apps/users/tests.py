from django.test import TestCase

# Create your tests here.
from django.core.cache import cache, caches

from makingsystem.settings.config import appid, appkey, sms_sjgn, template_id

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
ssender = SmsSingleSender(appid, appkey)
params = ["5678", 5]  # 当模板没有参数时，`params = []`
phone_numbers = ["13205827585", "17521125085"]
sms_type = 0
try:
  result = ssender.send_with_param(86, phone_numbers[0],
        template_id, params, sign=sms_sjgn, extend="", ext="")
  # result = ssender.send(sms_type, 86, "13205827585",
  #              "【腾讯云】您的验证码是: 5678", extend="", ext="")
except HTTPError as e:
  print(e)
except Exception as e:
  print(e)
print(result)


