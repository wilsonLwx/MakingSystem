# __author__ = 'wilsonLwx'
# __date__ = '2019/08/07'


import graphene
from graphene_django.debug import DjangoDebug

import users.schema


class Query(users.schema.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutations(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutations)
