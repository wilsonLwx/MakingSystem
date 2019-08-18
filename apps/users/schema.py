# __author__ = 'wilsonLwx'
# __date__ = '2019/08/08'
import random
import re

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


class InputData(graphene.InputObjectType):
    id = graphene.ID(required=True)
    old_pwd = graphene.String(required=True)
    new_pwd = graphene.String(required=True)


class ChangeInfo(graphene.Mutation):
    class Arguments:
        input_data = InputData(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        input_data = kwargs.get('input_data')
        pk = input_data.get('id')
        new_pwd = input_data.get('new_pwd')
        old_pwd = input_data.get('old_pwd')
        try:
            user_info = UserModel.objects.get(pk=pk)
        except Exception as e:
            raise GraphQLError('User is not existed, please check your input!')

        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        ok = user_info.check_password(old_pwd)
        if ok:
            user_info.set_password(new_pwd)
            user_info.save()
            ok = ok
            return ChangeInfo(ok=ok, user=user_info)
        else:
            raise GraphQLError('Password authentication failed!')


class RegisterData(graphene.InputObjectType):
    mobile = graphene.String(required=True)
    smsCode = graphene.String(required=True)


class Register(graphene.Mutation):
    class Arguments:
        registerData = RegisterData(required=True)

    result = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        register_data = kwargs.get('registerData')
        smsCode = register_data.get('smsCode')
        mobile = register_data.get('mobile')

        if not all([smsCode, mobile]):
            raise GraphQLError("有空信息输入")

        user_info = UserModel()
        if user_info.objects.filter(mobile=mobile):
            return Register(result=True, message="用户已注册")

        context = cache.get(mobile)
        if not context:
            return Register(result=False, message="验证码已过期")
        if smsCode != context:
            return Register(result=False, message="验证码不匹配，请重新输入")
        try:
            user = UserModel.objects.create(mobile=mobile)
        except db.IntegrityError:
            raise Exception("保存数据库失败")
        user.is_active = True
        user.save()
        # cache.delete('smsCode')
        return Register(result=True, message="用户保存成功")


class LoginData(graphene.InputObjectType):
    mobile = graphene.String(required=True)
    smsCode = graphene.String(required=True)

#
# class Login(graphene.Mutation):
#     class Arguments:
#         login_data = LoginData(required=True)
#
#     result = graphene.Boolean()
#     user = graphene.Field(UserType)
#     message = graphene.String()
#
#     def mutate(self, info, *args, **kwargs):
#         login_data = kwargs.get('login_data')
#         mobile = login_data.get('mobile')
#         smsCode = login_data.get('smsCode')
#         if not all([mobile, smsCode]):
#             raise GraphQLError("有空信息输入")
#         try:
#             user = UserModel.objects.get(mobile=mobile)
#         except Exception as e:
#             raise GraphQLError("手机号错误")
#         if not user.check_password(passwd):
#             raise GraphQLError("密码错误")
#         if not user.is_authenticated:
#             raise GraphQLError(f"{user}用户名或密码错误")
#         # login(info.context, user)
#         message = "登录成功"
#         return Login(result=True, user=user, message=message)


class WxauthorData(graphene.InputObjectType):
    code = graphene.String()
    openid = graphene.String()


class Wxauthor(graphene.Mutation):
    class Arguments:
         wxauthordata = WxauthorData(required=True)
    result = graphene.Boolean()
    openid = graphene.String()
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        code = kwargs.get('code', None)
        openid = kwargs.get('openid', None)
        user_info = UserModel()

        def search_user(openid):
            try:
                user = user_info.objects.get(openid=openid)
            except Exception as e:
                return False
            else:
                return user

        # 授权后 token 未过期，openid还在时
        if not code and openid:
            user = search_user(openid)
            if user:
                return Wxauthor(result=True, openid=user.openid, message="查询成功")
            else:
                return Wxauthor(result=False, openid=None, message="查询失败")

        # 用户未注册 或 token 过期
        if code and not openid:
            appid = ''
            appsecret = ''
            data = {
                'appid': appid,
                'appsecret': appsecret,
                'code': code
            }
            url = "https://api.weixin.qq.com/sns/jscode2session"
            r = requests.get(url, data=data, verify=True)
            if r.status_code != requests.codes.ok:
                raise GraphQLError(f"获取数据失败{r.text}")
            r_json = r.json()
            openid = r_json.get('openid')
            user = search_user(openid)

            # 查询到用户返回
            if user:
                return Wxauthor(result=True, openid=user.openid, message="用户已授权")

            # 未查询到用户保存到数据库
            else:
                user.openid = openid
                user.save()
                return Wxauthor(result=False, openid=openid, message="用户未授权")


class MobileVerifyData(graphene.InputObjectType):
    phoneNum = graphene.String(required=True)
    # verifyNum = graphene.String(required=True)


class MobileVerify(graphene.Mutation):
    class Arguments:
        mobileverifydata = MobileVerifyData(required=True)
    result = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        mobileverifydata = kwargs.get('mobileverifydata')
        phone_num = mobileverifydata.get('phoneNum')
        # verify_num = mobileverifydata.get('verifyNum')
        if not re.match(r'1[345678]\d{9}', phone_num):
            return MobileVerify(result=False, message="手机号码不是11位")
        # if not all([phone_num, verify_num]):
        #     return MobileVerify(result=False, message="参数不完整")
        # 查找数据库是否注册过
        user_info = UserModel()
        try:
            user = user_info.objects.get(mobile=phone_num)
        except Exception as e:
            LOG.info('用户未注册')
        else:
            if user is not None:
                return MobileVerify(result=True, message="用户已注册")

        # smsCode = '%06d' % random.randint(0, 999999)
        smsCode = '123456'
        if cache.get(phone_num):
            LOG.debug(cache.get(phone_num))
            return MobileVerify(result=True, message="验证码未过期")
        # try:
        #     ccp = CCP()
        #     result = ccp.sendTemplateSMS(phone_num, [smsCode, '5'], 1)
        # except Exception as e:
        #     LOG.error(e)
        #     return MobileVerify(result=False, message="发送短信异常")

        cache.set(phone_num, smsCode, 500)
        result = 0
        if result == 0:
            return MobileVerify(result=True, message="发送短信成功")
        else:
            return MobileVerify(result=False, message="发送短信失败")


class Mutation(graphene.ObjectType):
    change_info = ChangeInfo.Field()
    register = Register.Field()
    # login = Login.Field()
    wxauthor = Wxauthor.Field()
    mobileverify = MobileVerify.Field()