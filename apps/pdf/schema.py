import graphene
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from graphql import GraphQLError

from users.models import Users as UsersModel
from pdf.models import PDF as PDFModel
from utils.uploadaliyun import Xfer


class ReportInfo(graphene.ObjectType):
    url = graphene.String()
    pdf_name = graphene.String()


class ReportType(graphene.ObjectType):
    image = graphene.String()
    group = graphene.List(ReportInfo)


class Query(graphene.ObjectType):
    pdf_report = graphene.Field(ReportType, open_id=graphene.Int(required=True), page=graphene.Int(default_value=1))

    def resolve_pdf_report(self, info, open_id, page):
        user_obj = UsersModel.objects.filter(openid=open_id)
        group = []
        if user_obj.exists():
            image = user_obj.values('image').first().get('image')
            ret = PDFModel.objects.filter(user__in=user_obj).values('aliosspath', 'name', )
            r = ReportInfo()
            x = Xfer()
            x.initAliyun()
            for i in ret:
                path = i.get('aliosspath')
                pdf_name = i.get('name')
                url = x.sign_url(path)
                r.pdf_name = pdf_name
                r.url = url
                group.append(r)
            paginator = Paginator(group, 5)
            try:
                group = paginator.page(page)
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                group = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                raise GraphQLError('请求页数不存在')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                group = paginator.page(paginator.num_pages)

            x.clearAliyun()
            return ReportType(group=group, image=image)
        else:
            raise GraphQLError("User is not exist")
