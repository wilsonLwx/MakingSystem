# __author__ = 'wilsonLwx'
# __date__ = '2019/08/08'
import random
import re
import uuid
from graphql import GraphQLError
from utils.yuntongxun.SendTemplateSMS import CCP
from .models import Users as UserModel
from graphene_django import DjangoObjectType
import graphene
from django.core.cache import cache
from django import db
import requests
import logging

LOG = logging.getLogger(__file__)


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    pass


###################################################


class WxauthorData(graphene.InputObjectType):
    jsCode = graphene.String()


class Wxauthor(graphene.Mutation):
    """
    微信认证
    """

    class Arguments:
        wxauthordata = WxauthorData(required=True)

    result = graphene.Boolean()
    auth_token = graphene.String()
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        wxauthordata = kwargs.get('wxauthordata')
        js_code = wxauthordata.get('jsCode')

        def returnOpenid(js_code):
            appid = 'wx900ef66b9970c484'
            appsecret = '8ca28ffc3096a88b9f96d5f98cc272de'
            url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appsecret}&js_code={js_code}"
            r = requests.get(url, verify=True)
            if r.status_code != requests.codes.ok:
                raise GraphQLError(f"获取数据失败{r.text}")
            r_json = r.json()
            openid = r_json.get('openid')
            session_key = r_json.get('session_key')
            value = {
                'openid': openid,
                'session_key': session_key
            }
            return value

        # 使用uuid 产生token
        auth_token = uuid.uuid1()
        # 访问微信服务器获取openid
        value = returnOpenid(js_code)
        openid = value.get('openid')
        # 判断用户是否存在
        # result = UserModel.objects.filter(openid=openid, is_superuser=0).exists()
        # 如果 openid不存在报错
        if not openid:
            message = "openid为空"
            result = False
            return Wxauthor(result=result, auth_token=None, message=message)

        LOG.info(auth_token)
        message = "openid 获取成功"
        LOG.info(openid)
        # auth_token 存入redis 缓存
        cache.set(auth_token, value, 60 * 60 * 5)

        return Wxauthor(result=True, auth_token=auth_token, message=message)


class MobileVerifyData(graphene.InputObjectType):
    phoneNum = graphene.String(required=True)


class MobileVerify(graphene.Mutation):
    """
    发送手机验证码
    """

    class Arguments:
        mobileverifydata = MobileVerifyData(required=True)

    result = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        mobileverifydata = kwargs.get('mobileverifydata')
        phone_num = mobileverifydata.get('phoneNum')
        if not re.match(r'1[345678]\d{9}', phone_num):
            return MobileVerify(result=False, message="手机号码不是11位")
        # 生成验证码
        smsCode = '%06d' % random.randint(0, 999999)

        if cache.get(phone_num):
            LOG.debug(cache.get(phone_num))
            return MobileVerify(result=True, message="验证码未过期")
        # 发送验证码
        try:
            ccp = CCP()
            result = ccp.sendTemplateSMS(phone_num, [smsCode, '5'], 1)
        except Exception as e:
            LOG.error(e)
            return MobileVerify(result=False, message="发送短信异常")
        # 判断发送
        if result == 0:
            cache.set(phone_num, smsCode, 60 * 2)
            return MobileVerify(result=True, message="发送短信成功")
        else:
            cache.delete(phone_num)
            return MobileVerify(result=False, message="发送短信失败")


class RegisterData(graphene.InputObjectType):
    mobile = graphene.String(required=True)
    smsCode = graphene.String(required=True)
    auth_token = graphene.String(required=True)


class Register(graphene.Mutation):
    """
    验证手机号
    """

    class Arguments:
        registerData = RegisterData(required=True)

    result = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        register_data = kwargs.get('registerData')
        smsCode = register_data.get('smsCode')
        mobile = register_data.get('mobile')
        authToken = register_data.get('auth_token')
        # 判断是否输入空信息
        if not all([smsCode, mobile]):
            raise GraphQLError("有空信息输入")

        context = cache.get(mobile)
        value = cache.get(authToken)
        openid = value.get('openid')
        LOG.info(context, value)
        # user_info = UserModel.objects.filter(openid=openid)
        # if not user_info.exists():
        #     return Register(result=False, message="openid 未保存到数据库")
        # LOG.info(value)
        # 检查验证码
        if not context:
            return Register(result=False, message="验证码已过期")
        if smsCode != context:
            return Register(result=False, message="验证码不匹配，请重新输入")
        # 保存手机号
        userInfo = UserModel.objects.filter(mobile=mobile).first()
        # 判断用户是否存在
        if userInfo:
            # value = cache.get(authToken)
            # openid = value.get('openid')
            # userInfo.update(openid=openid)
            userInfo.username = mobile
            userInfo.mobile = mobile
            userInfo.openid = openid
            userInfo.save()
            return MobileVerify(result=True, message="用户信息已存在")

        try:
            UserModel.objects.create(
                username=mobile,
                openid=openid,
                mobile=mobile
            )
            # userInfo.username = mobile
            # userInfo.mobile = mobile
            # userInfo.openid = openid
            # userInfo.save()
        except db.IntegrityError:
            raise Exception("保存数据库失败")
        # cache.delete('smsCode')
        return Register(result=True, message="用户保存成功")


class SearchMobileData(graphene.InputObjectType):
    auth_token = graphene.String(required=True)


class SearchMobile(graphene.Mutation):
    """
    手机号是否验证
    """

    class Arguments:
        searchmobiledata = SearchMobileData(required=True)

    result = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        searchmobiledata = kwargs.get('searchmobiledata')
        auth_token = searchmobiledata.get('auth_token')

        value = cache.get(auth_token)
        openid = value.get('openid')

        userInfo = UserModel.objects.filter(openid=openid).first()
        if not userInfo:
            return SearchMobile(result=False, message="用户不存在")
        if not userInfo.mobile:
            return SearchMobile(result=False, message="手机号未验证")
        return SearchMobile(result=True, message=userInfo.mobile)


class Mutation(graphene.ObjectType):
    wxauthor = Wxauthor.Field()
    mobileverify = MobileVerify.Field()
    register = Register.Field()
    searchmobile = SearchMobile.Field()
