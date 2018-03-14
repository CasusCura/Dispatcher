"""Holds all classes that are related to issues that are active and need to be
handle by a nurse."""
from dispatcher.models.base import Base
import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from sqlalchemy.sql import func
from typing import Dict
import uuid


class IssueStates(enum.Enum):
    PENDING = 1
    QUEUED = 2
    CLOSED = 3
    CANCELLED = 4


class Issue(Base):
    """Represents a device or patient alerting the nurses to an issue or making
    a request for the nurses to help them with a need."""
    __tablename__ = 'issues'
    id = Column(String(32), primary_key=True)
    patientdevice = Column(String(32), ForeignKey('devices.id'))
    requesttype = Column(String(32), ForeignKey('requesttypes.id'))
    first_issued = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Enum(IssueStates), nullable=False)
    priority = Column(Integer, nullable=False)

    request = relationship('RequestType')
    device = relationship('Device')
    responses = relationship('Response',
                             order_by='desc(Response.eta)',
                             foreign_keys='id')

    data = relationship('RequestData',
                        order_by='desc(RequestData.timestamp)')

    def __init__(self, patientdeviceid: String, requesttype: String,
                 priority: int):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.patientdevice = patientdeviceid
        self.requesttype = requesttype
        self.priority = priority
        self.status = IssueStates.PENDING


class Response(Base):
    """Represents a nurse saying they will tend to this issue in a given amount
    of time. This will alert the patient and the other nurses how long until
    this nurse will be able to take care of this issue."""
    __tablename__ = 'responses'
    id = Column(String(32), primary_key=True)
    nursedevice = Column(String(32), ForeignKey('devices.id'))
    first_issued = Column(DateTime(timezone=True), server_default=func.now())
    data = Column(String)
    last_eta = Column(Integer, nullable=False)

    def __init__(self, nursedeviceid: String, eta: int, data: Dict):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.nursedevice = nursedeviceid
        self.last_eta = eta
        self.data = data


class RequestData(Base):
    """Allows devices to send data, or update fragments to an issue of any
    format. This allows for future expandability of devices."""
    __tablename__ = 'requestdata'
    id = Column(String(32), primary_key=True)
    patientdevice = Column(Integer, ForeignKey('devices.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    data = Column(String)

    def __init__(self, patientdevice: int, data: Dict):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.patientdevice = patientdevice.id
        self.data = data


class RequestType(Base):
    """This defines what kind've issue it is so that Nurses can read the type
    of issue and potentially reprioritize the issues they attempt to solve."""
    __tablename__ = 'requesttypes'
    id = Column(String(32), primary_key=True)
    deviceid = Column(Integer, nullable=False)
    devicetype = Column(String(32), ForeignKey('devicetypes.id'))
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    priority = Column(Integer, nullable=False)

    def __init__(self, id: int, name: String, description: String,
                 devicetype: String, priority: int):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.deviceid = id
        self.name = name
        self.description = description
        self.devicetype = devicetype
        self.priority = priority
