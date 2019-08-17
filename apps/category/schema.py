# __author__ = 'ly'
# __date__ = '2019/08/15'

import graphene
from graphene_django import DjangoObjectType

from makingsystem.settings import MEDIA_ROOT
from .models import TestDetails as TestDetailsModel
from .models import TestName as TestNameModel


class LeaderTestInfo(graphene.ObjectType):
    name = graphene.String()
    url = graphene.String()
    image = graphene.String()


class LeaderTestType(graphene.ObjectType):
    group = graphene.List(LeaderTestInfo)


class Query:
    leader_test = graphene.Field(LeaderTestType)

    def resolve_leader_test(self, info):
        banners_obj = TestDetailsModel.objects.filter(is_index_show=True)
        banner_info = banners_obj.values_list('parent_test_name__name', 'url', 'image')
        return LeaderTestType(group=[LeaderTestInfo(name=i[0], url=i[1], image=i[2]) for i in banner_info])
