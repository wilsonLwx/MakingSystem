#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from .CCPRestSDK import REST
import ConfigParser
import logging
LOG = logging.getLogger(__file__)
#主帐号
accountSid= '您的主帐号'

#主帐号Token
accountToken= '您的主帐号Token'

#应用Id
appId='您的应用ID'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id


class CCP(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            obj = super().__new__()
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls.instance = obj
        return cls.instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to,datas,tempId)
        except Exception as e:
            LOG.error(e)
            raise e
        status_Code = result.get('statusCode')

        return 0 if status_Code == '000000' else -1

ccp = CCP()

   
#sendTemplateSMS(手机号码,内容数据,模板Id)