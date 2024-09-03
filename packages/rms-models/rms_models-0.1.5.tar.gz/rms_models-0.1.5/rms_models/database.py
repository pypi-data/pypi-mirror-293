from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_engine(connection_string: str):
    return create_engine(connection_string)


def get_session(engine):
    pass
