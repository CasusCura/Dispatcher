from sqlalchemy import Column, Integer, String
from dispatcher.models.base import Base
import uuid


class User(Base):
    __tablename__ = 'users'
    id = Column(String(32), name='id', primary_key=True)
    username = Column(String, nullable=False)
    # PLZ FIX
    password = Column(String, nullable=False)
    discriminator = Column(String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}


class Nurse(User):
    __mapper_args__ = {'polymorphic_identity': 'nurse'}
    floor = Column(Integer, nullable=True)

    def __init__(self, username: String, password: String, floor: String):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.username = username
        self.password = password
        self.floor = floor
        self.discriminator = 'nurse'


class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}
    title = Column(String(50))

    def __init__(self, username: String, password: String, title: String):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.username = username
        self.password = password
        self.title = title
        self.discriminator = 'admin'
