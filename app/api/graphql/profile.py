import strawberry
from strawberry.fastapi import GraphQLRouter

from app.api.graphql.profile_schema import ProfileQuery

graphql_profiles = GraphQLRouter(strawberry.Schema(ProfileQuery), graphiql=True)
