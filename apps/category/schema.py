# __author__ = 'ly'
# __date__ = '2019/08/15'
from datetime import datetime
import graphene

from .models import Banner as BannerModel
from .models import TestDetails as TestDetailsModel


class LeaderTestInfo(graphene.ObjectType):
    url = graphene.String()
    title = graphene.String()
    image = graphene.String()


class LeaderTestType(graphene.ObjectType):
    group = graphene.List(LeaderTestInfo)


class Query:
    leader_test = graphene.Field(LeaderTestType)
    courses = graphene.Field(LeaderTestType)

    def resolve_leader_test(self, info):
        leader_test_obj = TestDetailsModel.objects.filter(is_index_show=True, push_time__lt=datetime.now())
        banner_info = leader_test_obj.values_list('title', 'url', 'image')
        return LeaderTestType(group=[LeaderTestInfo(title=i[0], url=i[1], image=i[2]) for i in banner_info])

    def resolve_courses(self, info):
        banner_obj = BannerModel.objects.filter(is_show=True, push_time__lt=datetime.now())
        banner_info = banner_obj.values_list('title', 'url', 'image')
        return LeaderTestType(group=[LeaderTestInfo(title=i[0], url=i[1], image=i[2]) for i in banner_info])
