from dispatcher.models import (Device,
                               DeviceType,
                               PatientDevice,
                               PatientDeviceType,
                               NurseDevice,
                               NurseDeviceType,
                               Response,
                               RequestType,
                               Issue)
from typing import Dict


class ModelCreationMixin(object):

    def create_patient_device_type(self, name: str='test_p_dev_t',
                                   desc: str='test',
                                   session=None):
        p = PatientDeviceType(name, desc)
        if session:
            session.add(p)
        return p

    def create_nurse_device_type(self, name: str='test_n_dev_t',
                                 desc: str='test',
                                 session=None):
        p = NurseDeviceType(name, desc)
        if session:
            session.add(p)
        return p

    def create_requesttype(self, device_type: PatientDeviceType,
                           id: str='TEST',
                           desc: str='test',
                           priority: int=0,
                           session=None):
        p = RequestType(id, desc, device_type.id, priority)
        if session:
            session.add(p)
        return p

    def create_patient_device(self, device_type: DeviceType,
                              location: str='test:1',
                              serial_number: str='DEFAULT',
                              session=None):
        p = PatientDevice(device_type.id, location, serial_number)
        if session:
            session.add(p)
        return p

    def create_nurse_device(self, device_type: DeviceType,
                            floor: str='test:1',
                            session=None):
        p = NurseDevice(device_type.id, floor)
        if session:
            session.add(p)
        return p

    def create_response(device: NurseDevice,
                        issue: Issue,
                        eta: int,
                        data: Dict,
                        session=None):
        p = Response(device.id, eta, issue.id, data)
        if session:
            session.add(p)
        return p

    def create_issue(self, device: PatientDevice, request: RequestType,
                     session=None):
        iss = Issue(device.id, request.id, request.priority)
        if session:
            session.add(iss)
        return iss
