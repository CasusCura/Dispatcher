from dispatcher import models


def init_db(factory):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    models.Base.metadata.create_all(bind=factory.engine)
