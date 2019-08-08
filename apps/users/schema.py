# __author__ = 'wilsonLwx'
# __date__ = '2019/08/08'
from .models import Users as UserModel
from graphene_django import DjangoObjectType
import graphene


class User(DjangoObjectType):
    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    users = graphene.List(User)

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()
