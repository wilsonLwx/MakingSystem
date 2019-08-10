# __author__ = 'wilsonLwx'
# __date__ = '2019/08/07'


import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

import users.schema


class Query(users.schema.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutations(users.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutations)
