# __author__ = 'ly'
# __date__ = '2019/08/15'

import graphene
from graphene_django import DjangoObjectType

from .models import TestDetails as TestDetailsModel
from .models import TestName as TestNameModel


class TestNameType(graphene.ObjectType):
    names = graphene.List(graphene.String)
    urls = graphene.List(graphene.String)


class Query:

    banners = graphene.Field(TestNameType)

    def resolve_banners(self, info):
        banners_obj = TestDetailsModel.objects.filter(is_index_show=True)
        banner_names = banners_obj.values_list('parent_test_name__name', flat=True)
        banner_urls = banners_obj.values_list('url', flat=True)
        return TestNameType(names=banner_names, urls=banner_urls)
