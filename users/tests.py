from unittest import TestCase

from sqlalchemy import Engine, create_engine, delete
from sqlalchemy.orm import Session
from core.settings import DECLARATIVE_BASE
from core.schema import schema

from users.models import User, create_user, delete_user, get_all_users


class DB:
    def __init__(self, engine: Engine, session: Session) -> None:
        self.engine: Engine = engine
        self.session: Session = session


def set_up_test_db() -> DB: 
    print("Setting up database")
    engine = create_engine("sqlite://", echo=False)
    session = Session(engine)
    DECLARATIVE_BASE.metadata.create_all(engine)
    return DB(engine, session)


def clean_up_test_db(engine: Engine):
    print("Cleaning up database")
    DECLARATIVE_BASE.metadata.drop_all(engine)


class TestUsersModels(TestCase):
    def setUp(self) -> None:
        db = set_up_test_db()
        self.session = db.session
        self.engine = db.engine
        return super().setUp()

    def test_create_user(self):
        new_user = create_user(
                db=self.session,
                first_name="Test",
                last_name="User",
                email="test@email.com")
        self.assertIsNotNone(new_user)
        self.assertEqual(str(new_user.first_name), "Test")

    def test_get_all_users(self):
        users = get_all_users(db=self.session)
        self.assertIsNotNone(users)

    def tearDown(self) -> None:
        clean_up_test_db(self.engine)
        return super().tearDown()


class TestUsersQueries(TestCase):
    def setUp(self) -> None:
        db = set_up_test_db()
        self.session = db.session
        self.engine = db.engine
        return super().setUp()

    def test_query_all_users(self):
        query = """
            query AllUsers {
              allUsers {
                id
                firstName
                lastName
                email
                __typename
              }
            }
        """
        result = schema.execute_sync(query)
        self.assertIsNotNone(result)
        self.assertIsNone(result.errors)


    def test_new_user(self):
        query = """
            mutation AddUser($firstName: String!, $lastName: String!, $email: String!) {
              newUser (firstName: $firstName, lastName: $lastName, email: $email) {
                id
                firstName
                lastName
                email
                __typename
              }
            }
        """
        result = schema.execute_sync(
            query,
            variable_values={
              "firstName": "Testing",
              "lastName": "Man",
              "email": "code@test.com"
            }
        )
        print("result", result)
        self.assertIsNotNone(result)
        self.assertIsNone(result.errors)
        if result.data:
            self.assertIsNotNone(str(result.data.get("newUser")))


    def test_delete_users(self):
        delete_user(User.first_name == "Testing", db=self.session)


    def tearDown(self) -> None:
        clean_up_test_db(self.engine)
        return super().tearDown()
