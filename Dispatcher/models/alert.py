from dispatcher.models import Base


class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    alertype = Column(Integer, ForeignKey('user.id'))
