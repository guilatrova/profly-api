import graphene
import savings.schema


class Query(savings.schema.Query, graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


schema = graphene.Schema(query=Query)
