"""Holds all classes that are related to issues that are active and need to be
handle by a nurse."""
from dispatcher.models.base import Base
import enum
import json
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
    time_updated = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now())
    status = Column(Enum(IssueStates), nullable=False)
    priority = Column(Integer, nullable=False)

    request = relationship('RequestType')
    device = relationship('PatientDevice')
    responses = relationship('Response',
                             order_by='Response.last_eta',
                             primaryjoin='Response.issueid==Issue.id')

    data = relationship('RequestData',
                        order_by='RequestData.timestamp',
                        primaryjoin='RequestData.issueid==Issue.id')

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
    issueid = Column(String(32), ForeignKey('issues.id'))
    nursedevice = Column(String(32), ForeignKey('devices.id'))
    first_issued = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(),
                          onupdate=func.now())
    data = Column(String)
    last_eta = Column(Integer, nullable=False)

    device = relationship('Device')
    issue = relationship('Issue')

    def __init__(self, nursedeviceid: String, eta: int, issueid: String,
                 data: Dict):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.issueid = issueid
        self.nursedevice = nursedeviceid
        self.last_eta = eta
        self.data = json.dumps(data)


class RequestData(Base):
    """Allows devices to send data, or update fragments to an issue of any
    format. This allows for future expandability of devices."""
    __tablename__ = 'requestdata'
    id = Column(String(32), primary_key=True)
    issueid = Column(String(32), ForeignKey('issues.id'))
    patientdevice = Column(String(32), ForeignKey('devices.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    data = Column(String)

    def __init__(self, patientdevice: String, issueid: String, data: Dict):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.issueid = issueid
        self.patientdevice = patientdevice
        self.data = json.dumps(data)


class RequestType(Base):
    """This defines what kind've issue it is so that Nurses can read the type
    of issue and potentially reprioritize the issues they attempt to solve."""
    __tablename__ = 'requesttypes'
    id = Column(String(32), primary_key=True)
    device_request_id = Column(String, nullable=False)
    devicetype = Column(String(32), ForeignKey('devicetypes.id'))
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    priority = Column(Integer, nullable=False)

    def __init__(self, id: String, name: String, description: String,
                 devicetype: String, priority: int):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.device_request_id = id
        self.name = name
        self.description = description
        self.devicetype = devicetype
        self.priority = priority
