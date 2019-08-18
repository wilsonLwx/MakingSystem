import graphene


class ReportInfo(graphene.ObjectType):
    image = graphene.String()


class Query(graphene.ObjectType):
    pass
