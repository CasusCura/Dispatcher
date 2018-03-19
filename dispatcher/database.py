from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dispatcher import models


engine = create_engine('sqlite:///:memory:', convert_unicode=True)


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    models.Base.metadata.create_all(bind=engine)


def get_session():
    DBSession = sessionmaker(bind=engine)
    return DBSession()
