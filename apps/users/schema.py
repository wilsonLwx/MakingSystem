# __author__ = 'wilsonLwx'
# __date__ = '2019/08/08'

from graphql import GraphQLError
from .models import Users as UserModel
from graphene_django import DjangoObjectType
import graphene

from .forms import RegisterForm
# from django.contrib.auth import authenticate,login,logout

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


# class Login_Data(graphene.InputObjectType):
#     name = graphene.String(required=True)
#     passwd = graphene.String(required=True)
#
#
# class Login(graphene.Mutation):
#     class Arguments:
#         login_data = Login_Data(required=True)
#
#     ok = graphene.Boolean()
#     user = graphene.Field(UserType)
#
#     def mutate(self, info, *args, **kwargs):
#         login_data = kwargs.get('login_data')
#         loginfrom = LoginForm(info.context)
#         if loginfrom.is_valid():
#             name = login_data.get('name')
#             passwd = login_data.get('passwd')
#             user = authenticate(name=name, passwd=passwd)
#             if user is not None:
#                 if user.is_active:
#                     login(info.context, user)
#                     return Login(ok=True, user=user)
#             else:
#                 raise GraphQLError("login failed")

class RegisterData(graphene.InputObjectType):
    name = graphene.String(required=True)
    passwd = graphene.String(required=True)
    mobile = graphene.Int(required=True)


class Register(graphene.Mutation):
    class Arguments:
        register_data = RegisterData(required=True)
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        register_data = kwargs.get("register_data")
        registerform = RegisterForm(info.context.POST)
        if registerform.is_valid():
            mobile = register_data.get('moblie')
            if UserModel.objects.filter(mobile=mobile):
                return Register(ok=True, user=mobile)
            name = register_data.get('name')
            passwd = register_data.get('passwd')
            mobile = register_data.get('mobile')
            try:
                user = UserModel.objects.create_user(
                    name=name, password=passwd, mobile=mobile
                )
                # user.name = name
                # user.set_password(passwd)
                # user.mobile = mobile
                user.save()
                ok = True
            except Exception as e:
                ok = False
                raise Exception(f"mysql write fail {e}")
            return Register(ok=ok, user=user)


class Mutation(graphene.ObjectType):
    change_info = ChangeInfo.Field()
    register = Register.Field()
