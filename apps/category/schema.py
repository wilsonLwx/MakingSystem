# __author__ = 'ly'
# __date__ = '2019/08/15'
from datetime import datetime

import graphene
from graphene_django import DjangoObjectType

from .models import TestDetails as TestDetailsModel
from .models import Banner as BannerModel


class LeaderTestInfo(graphene.ObjectType):
    name = graphene.String()
    url = graphene.String()
    image = graphene.String()


class LeaderTestType(graphene.ObjectType):
    group = graphene.List(LeaderTestInfo)


class BannerType(DjangoObjectType):
    class Meta:
        model = BannerModel


class Query:
    leader_test = graphene.Field(LeaderTestType)
    banner = graphene.Field(BannerType)

    def resolve_leader_test(self, info):
        banners_obj = TestDetailsModel.objects.filter(is_index_show=True, push_time__lt=datetime.now())
        banner_info = banners_obj.values_list('parent_test_name__name', 'url', 'image')
        return LeaderTestType(group=[LeaderTestInfo(name=i[0], url=i[1], image=i[2]) for i in banner_info])

    def resolve_banner(self, info):
        return BannerModel.objects.filter(is_show=True, push_time__lt=datetime.now())
