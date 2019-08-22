# graphql语法
import graphene
from graphene_django import DjangoObjectType

# UseraModel的用法跟django模型类一个用法 object 进行增删改查
from graphql import GraphQLError

from apps.users.models import Users as UserModel
from uploadaliyun import Xfer


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel


# --------------------------------------------------------------------------
# 一.从页面获取内容的形式：注册页面 (post)

# 1.先定义要获取的内容的格式 继承 graphene.InputObjectType
"""
1.定义获取数据的类  
2.定义处理数据的类  
3.在处理数据的类里面 实例化一个 获取数据的类 得到类属性及获取的数据
4.在处理数据的类里面 定义类属性 作为返回数据
5.返回处理数据类的实例化
"""


class InputData(graphene.InputObjectType):
    id = graphene.ID(required=True)
    old_pwd = graphene.String(required=True)
    new_pwd = graphene.String(required=True)
    username = graphene.String(required=True)


# 2.定义获取数据后的处理类 继承 graphene.Mutation
class Handler(graphene.Mutation):
    class Arguments:
        # 实例化上面定义的数据类  标准步骤
        input_data = InputData(required=True)

    # 定义要返回的数据及其格式
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    # 定义处理方法,info 对应 django的 request参数 必须有
    # 方法名 mutate 类似 post 作用
    def mutate(self, info, *args, **kwargs):
        input_data = kwargs.get('input_data')  # 此处对应实例化的 类名
        # 根据 实例化的类 来获取数据
        id = input_data.get('id')
        old_pwd = input_data.get('old_pwd')
        new_pwd = input_data.get('new_pwd')
        username = input_data.get('username')
        # 这里得到的user 就是 request.user 用来使用django自带的认证
        user = info.context.user
        ok = 'ok'

        # 返回处理的类的实例化
        return Handler(ok=ok, user=user)


# -----------------------------------------------------------------------------------

# 二,查询页面的返回即 get
# 1.定义返回的数据类
class ReportInfo(graphene.ObjectType):
    url = graphene.String()
    name = graphene.String()


# 2.定义要返回的数据的格式类
class ReportType(graphene.ObjectType):
    # 数据以 list 形式返回
    group = graphene.List(ReportInfo)


from apps.users.models import Users as UsersModel
from apps.pdf import PDF as PDFModel


# 3.定义处理类 (一个类属性对应一个get请求和一个 def resolve_(类属性名字)方法)
class Query(graphene.ObjectType):
    pdf_report = graphene.Field(ReportType, open_id=graphene.Int(required=True))

    # xxx = jjjjj   (上面需要定义一个数据类型的类，和一个返回数据的类型的类)

    # 参1：info 必带  参2：参数(前端传过来)
    def resolve_pdf_report(self, info, open_id):
        user_obj = UsersModel.objects.filter(openid=open_id)
        group = []  # 前面定义的返回类型是List
        if user_obj.exists():
            ret = PDFModel.objects.filter(user__in=user_obj).values('aliosspath', 'name')
            r = ReportInfo()
            x = Xfer()
            x.initAliyun()
            for i in ret:
                path = i.get('aliosspath')
                name = i.get('name')
                url = x.sign_url(path)
                r.name = name
                r.url = url
                group.append(r)
            x.clearAliyun()
        else:
            raise GraphQLError("User is not exist")

        # 返回数据类型的类
        return ReportType(group=group)

    # def resolve_xxx(self, info):
    #     return (定义的返回的数据类的实例化)
