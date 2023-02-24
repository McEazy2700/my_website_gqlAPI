from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from decouple import config


db_url = URL.create(
        drivername="postgresql",
        host=str(config("PGHOST")),
        username=str(config("PGUSER")),
        password=str(config("PGPASSWORD")),
        port=int(config("PGPORT")),
        database=str(config("PGDATABASE"))
    )


class Base(DeclarativeBase):
    pass


engine = create_engine(db_url, echo=True)
session = Session(engine)
