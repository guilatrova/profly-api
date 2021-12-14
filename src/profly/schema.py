import graphene

import savings.schema
import stocks.schema


class Query(stocks.schema.Query, savings.schema.Query, graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


class Mutation(stocks.schema.Mutation, savings.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
