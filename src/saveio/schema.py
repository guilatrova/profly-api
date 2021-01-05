import graphene

import savings.schema


class Query(savings.schema.Query, graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


class Mutation(savings.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
