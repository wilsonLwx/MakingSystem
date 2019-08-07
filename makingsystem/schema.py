# __author__ = 'wilsonLwx'
# __date__ = '2019/08/07'


import graphene
from graphene_django.debug import DjangoDebug


class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query)
