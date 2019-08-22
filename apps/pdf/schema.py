import graphene
from graphql import GraphQLError

from users.models import Users as UsersModel
from pdf.models import PDF as PDFModel
from utils.uploadaliyun import Xfer


class ReportInfo(graphene.ObjectType):
    url = graphene.String()
    name = graphene.String()


class ReportType(graphene.ObjectType):
    group = graphene.List(ReportInfo)


class Query(graphene.ObjectType):
    pdf_report = graphene.Field(ReportType, open_id=graphene.Int(required=True))

    def resolve_pdf_report(self, info, open_id):
        user_obj = UsersModel.objects.filter(openid=open_id)
        group = []
        if user_obj.exists():
            ret = PDFModel.objects.filter(user__in=user_obj).values('aliosspath', 'name')
            r = ReportInfo()
            x = Xfer()
            x.initAliyun()
            for i in ret:
                path = i.get('aliosspath')
                name = i.get('name')
                url = x.sign_url(path)
                r.name = name
                r.url = url
                group.append(r)
            x.clearAliyun()
        else:
            raise GraphQLError("User is not exist")

        return ReportType(group=group)
