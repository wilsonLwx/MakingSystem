#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from .CCPRestSDK import REST
import ConfigParser
import logging
LOG = logging.getLogger(__file__)
#���ʺ�
accountSid= '�������ʺ�'

#���ʺ�Token
accountToken= '�������ʺ�Token'

#Ӧ��Id
appId='����Ӧ��ID'

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'

#����˿� 
serverPort='8883'

#REST�汾��
softVersion='2013-12-26'

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id


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

   
#sendTemplateSMS(�ֻ�����,��������,ģ��Id)