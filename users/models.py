from typing import Sequence
from sqlalchemy import select, String
from sqlalchemy.orm import Mapped, Session, mapped_column
from core.settings import DECLARATIVE_BASE, DB_SESSION as session


class User(DECLARATIVE_BASE):
    __tablename__ = "user_acount"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"""
            User(id={self.id},
            first_name={self.first_name},
            last_name={self.last_name},
            email={self.email})"""


def get_all_users(session: Session=session) -> Sequence[User]:
    statement = select(User)
    return session.scalars(statement).all()


def create_user(first_name: str, last_name: str, email: str, session: Session = session) -> User:
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
