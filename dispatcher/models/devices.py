"""Holds all classes related to defining both nurse and patient devices."""
from dispatcher.models.base import Base
import enum
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
import uuid


class DeviceStatus(enum.Enum):
    INACTIVE = 0
    ACTIVE = 1
    DEACTIVATED = 2
    RETIRED = 3


class Device(Base):
    """Represents any device that needs to have credentials managed for
    authentication to the WPA2 network."""
    __tablename__ = 'devices'

    id = Column(String(32), primary_key=True)
    devicetype = Column(String(32), ForeignKey('devicetypes.id'))
    status = Column(Enum(DeviceStatus), nullable=False)
    used_by = Column(String(10))
    __mapper_args__ = {'polymorphic_on': used_by}

    def serialize(self, **kwargs):
        return {
            'id': id,
            'devicetype': self.devicetype,
            'status': self.status,
            'used_by': self.used_by,
            **kwargs
        }


class PatientDevice(Device):
    """Represents an individual patient device. This is associated with one or
    many patients but is identified to nurses via its location."""
    location = Column(String(50))
    issues = relationship('Issue',
                          primaryjoin='Device.id == \
                          Issue.patientdevice')
    __mapper_args__ = {'polymorphic_identity': 'patientdevice'}

    def __init__(self, devicetype: String, location: String):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.devicetype = devicetype
        self.status = DeviceStatus.INACTIVE
        self.location = location

    def serialize(self):
        super(PatientDevice, self)\
            .serialize(location=self.location)


class NurseDevice(Device):
    floor = Column(String(50))
    responses = relationship('Response',
                             order_by='Response.first_issued',
                             primaryjoin='NurseDevice.id == \
                             Response.nursedevice')
    __mapper_args__ = {'polymorphic_identity': 'nursedevice'}

    def __init__(self, devicetype: String, floor: String):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.devicetype = devicetype
        self.status = DeviceStatus.INACTIVE
        self.floor = floor

    def serialize(self):
        super(NurseDevice, self)\
            .serialize(floor=self.floor)


class DeviceType(Base):
    __tablename__ = 'devicetypes'

    id = Column(String(32), primary_key=True)
    product_name = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    discriminator = Column('devicetype', String(50))
    devices = relationship('Device',
                           primaryjoin='DeviceType.id == Device.devicetype',
                           foreign_keys='Device.devicetype')
    __mapper_args__ = {'polymorphic_on': discriminator}

    def serialize(self, **kwargs):
        return {
            'id': self.id,
            'product_name': self.devicetype,
            'product_description': self.description,
            'devicetype': self.discriminator,
            **kwargs
        }


class NurseDeviceType(DeviceType):
    __mapper_args__ = {'polymorphic_identity': 'nursedevice'}
    devices = relationship('Device')

    def __init__(self, name: String, description: String):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.name = name
        self.description = description


class PatientDeviceType(DeviceType):
    requesttypes = relationship('RequestType')
    devices = relationship('Device')
    __mapper_args__ = {'polymorphic_identity': 'patientdevice'}

    def __init__(self, name: String, description: String):
        self.id = str(uuid.uuid4().hex).encode('ascii')
        self.name = name
        self.description = description
