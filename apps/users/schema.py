# __author__ = 'wilsonLwx'
# __date__ = '2019/08/08'

from graphql import GraphQLError
from .models import Users as UserModel
from graphene_django import DjangoObjectType
import graphene
from django import db
import requests


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()


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
    name = graphene.String(required=True)
    passwd = graphene.String(required=True)
    mobile = graphene.String(required=True)


class Register(graphene.Mutation):
    class Arguments:
        register_data = RegisterData(required=True)

    result = graphene.Boolean()
    user = graphene.Field(UserType)
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        register_data = kwargs.get('register_data')
        name = register_data.get('name')
        passwd = register_data.get('passwd')
        mobile = register_data.get('mobile')
        user_info = UserModel.objects.filter(mobile=mobile)
        if user_info:
            message = "用户已注册"
            return Register(reslut=False, user=user_info, message=message)

        if not all([name, passwd, mobile]):
            raise GraphQLError("有空信息输入")

        try:
            user = UserModel.objects.create_user(username=name, password=passwd, mobile=mobile)
        except db.IntegrityError:
            raise Exception("保存数据库失败")
        user.is_active = False
        user.save()
        message = "数据库保存成功"
        return Register(result=True, user=user, message=message)


class LoginData(graphene.InputObjectType):
    mobile = graphene.String(required=True)
    passwd = graphene.String(required=True)


class Login(graphene.Mutation):
    class Arguments:
        login_data = LoginData(required=True)

    result = graphene.Boolean()
    user = graphene.Field(UserType)
    message = graphene.String()

    def mutate(self, info, *args, **kwargs):
        login_data = kwargs.get('login_data')
        mobile = login_data.get('mobile')
        passwd = login_data.get('passwd')
        if not all([mobile, passwd]):
            raise GraphQLError("有空信息输入")
        try:
            user = UserModel.objects.get(mobile=mobile)
        except Exception as e:
            raise GraphQLError("手机号错误")
        if not user.check_password(passwd):
            raise GraphQLError("密码错误")
        if not user.is_authenticated:
            raise GraphQLError(f"{user}用户名或密码错误")
        # login(info.context, user)
        message = "登录成功"
        return Login(result=True, user=user, message=message)


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


class Mutation(graphene.ObjectType):
    change_info = ChangeInfo.Field()
    register = Register.Field()
    login = Login.Field()
    wxauthor = Wxauthor.Field()
