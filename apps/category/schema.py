
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


class Mutation(graphene.ObjectType):
    change_info = ChangeInfo.Field()
