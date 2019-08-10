# __author__ = 'wilsonLwx'
# __date__ = '2019/08/08'

from graphql import GraphQLError
from .models import Users as UserModel
from graphene_django import DjangoObjectType
import graphene


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()


class ChangeInfo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        old_pwd = graphene.String(required=True)
        new_pwd = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        pk = kwargs.get('id')
        new_pwd = kwargs.get('new_pwd')
        old_pwd = kwargs.get('old_pwd')
        try:
            user_info = UserModel.objects.get(pk=pk)
        except Exception as e:
            raise GraphQLError('User is not existed, please check your input!')
        ok = user_info.check_password(old_pwd)
        if ok:
            user_info.set_password(new_pwd)
            user_info.save()
            ok = ok
            return ChangeInfo(ok=ok, user=user_info)
        else:
            raise GraphQLError('Password authentication failed!')


class Mutation(graphene.ObjectType):
    change_info = ChangeInfo.Field()
