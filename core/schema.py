import strawberry
from core.settings import DB_ENGINE, DECLARATIVE_BASE

from users.schema import UserMutation, UsersQuery

DECLARATIVE_BASE.metadata.create_all(DB_ENGINE)


@strawberry.type
class Query(UsersQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
