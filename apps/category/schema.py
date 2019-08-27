# __author__ = 'ly'
# __date__ = '2019/08/15'

import graphene
from graphene_django.types import DjangoObjectType
from utils.uploadaliyun import Xfer
from .models import TestDetails as TestDetailsModel
from .models import TestName as TestNameModel
from .models import Banner as BannerModel
from .models import TestIn as TestInModel
from .models import SlideShow as SlideshowModel
from .models import AboutUs as AboutUsModel
from datetime import datetime


class TestInType(DjangoObjectType):
    class Meta:
        model = TestInModel


class SlideShowInfo(graphene.ObjectType):
    title = graphene.String()
    image = graphene.String()


class AboutUsType(DjangoObjectType):
    class Meta:
        model = AboutUsModel


class LeaderTestInfo(graphene.ObjectType):
    url = graphene.String()
    title = graphene.String()
    image = graphene.String()


class TestDetailInfo(LeaderTestInfo):
    test_number = graphene.Int()
    test_dec = graphene.String()


class TestDetailType(graphene.ObjectType):
    group = graphene.List(TestDetailInfo)


class LeaderTestType(graphene.ObjectType):
    group = graphene.List(LeaderTestInfo)


class SlideShowType(graphene.ObjectType):
    group = graphene.List(SlideShowInfo)


class Query(graphene.ObjectType):
    leader_test = graphene.Field(TestDetailType)
    courses = graphene.Field(LeaderTestType)
    indexbanners = graphene.Field(LeaderTestType)
    test_in = graphene.Field(TestInType, title=graphene.String(required=True))
    slideshow = graphene.Field(SlideShowType)

    def resolve_slideshow(self, info):
        """首页轮播图"""
        slideshow_obj = SlideshowModel.objects.all()
        slideshow_info = slideshow_obj.values_list('title', 'image')
        group = []
        x = Xfer()
        x.initAliyun()
        for i in slideshow_info:
            title = i[0]
            image = x.sign_url(i[1])
            group.append(SlideShowInfo(title=title, image=image))
        return SlideShowType(group=group)

    def resolve_leader_test(self, info):
        """首页测试"""
        leader_test_obj = TestDetailsModel.objects.filter(is_index_show=True, push_time__lt=datetime.now())
        banner_info = leader_test_obj.values_list('title', 'url', 'image', 'test_number', 'test_dec')
        group = []
        x = Xfer()
        x.initAliyun()
        for i in banner_info:
            title = i[0]
            url = i[1]
            image = x.sign_url(i[2])
            test_number = i[3]
            test_dec = i[4]
            group.append(TestDetailInfo(title=title, url=url, image=image, test_number=test_number, test_dec=test_dec))

        return TestDetailType(group=group)

    def resolve_courses(self, info):
        # 首页---课程分类
        banner_obj = BannerModel.objects.filter(is_show=True, push_time__lt=datetime.now())
        banner_info = banner_obj.values_list('title', 'url', 'image')
        group = []
        x = Xfer()
        x.initAliyun()
        for i in banner_info:
            title = i[0]
            url = i[1]
            image = x.sign_url(i[2])
            group.append(LeaderTestInfo(title=title, url=url, image=image))

        return LeaderTestType(group=group)

    # def resolve_indexbanners(self, info):
    #     # 首页 第一部分 轮播图
    #
    #     name_list = TestNameModel.objects.filter(is_index_show=True).values_list('name')
    #     leader_test_obj = TestDetailsModel.objects.filter(is_index_show=True, push_time__lt=datetime.now(),
    #                                                       child_test_name__name__in=name_list)
    #     banner_info = leader_test_obj.values_list('title', 'url', 'image')
    #     group = []
    #     x = Xfer()
    #     x.initAliyun()
    #     for i in banner_info:
    #         title = i[0]
    #         url = i[1]
    #         image = x.sign_url(i[2])
    #         group.append(LeaderTestInfo(title=title, url=url, image=image))
    #     return LeaderTestType(group=group)

    def resolve_test_in(self, info, title):
        return TestInModel.objects.filter(title=title).first()

    def resolve_about_us(self, info):
        return AboutUsModel.objects.all().first()
