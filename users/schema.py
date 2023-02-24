from typing import List
import strawberry

from users.models import create_user, get_all_users


@strawberry.type(description="The user account type")
class UserType:
    id: int
    first_name: str
    last_name: str
    email: str


@strawberry.type
class UsersQuery:
    @strawberry.field
    def all_users() -> List[UserType]:
        users: List[UserType] = []
        for user in get_all_users():
            users.append(UserType(id=user.id,
                                  first_name=user.first_name,
                                  last_name=user.last_name,
                                  email=user.email))
        return users


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def new_user(self,
                 first_name: str, last_name: str, email: str) -> UserType:
        new_user = create_user(
                first_name=first_name,
                last_name=last_name, email=email)
        print(new_user)
        return UserType(id=new_user.id,
                        first_name=new_user.first_name,
                        last_name=new_user.last_name,
                        email=new_user.email)
