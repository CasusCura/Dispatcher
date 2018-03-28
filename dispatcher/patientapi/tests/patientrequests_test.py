from unittest import TestCase
import unittest
import pdb
import urllib
import os
from typing import Dict
from tornado.options import options
from tornado.httpserver import HTTPServer
from tornado.httpclient import HTTPClient
from tornado.ioloop import IOLoop
from dispatcher import Dispatcher
from run import create_router
from collections import OrderedDict


from dispatcher.models import (DeviceType,
                               PatientDevice,
                               PatientDeviceType,
                               NurseDevice,
                               NurseDeviceType,
                               Response,
                               RequestType,
                               Issue)


def create_patient_device_type(name: str='test_p_dev_t',
                               desc: str='test',
                               session=None):
    p = PatientDeviceType(name, desc)
    if session:
        session.add(p)
    return p


def create_nurse_device_type(name: str='test_n_dev_t',
                             desc: str='test',
                             session=None):
    p = NurseDeviceType(name, desc)
    if session:
        session.add(p)
    return p


def create_requesttype(device_type: PatientDeviceType,
                       id: str='TEST',
                       name: str='test_p_dev_t',
                       desc: str='test',
                       priority: int=0,
                       session=None):
    p = RequestType(id, name, desc, device_type.id, priority)
    if session:
        session.add(p)
    return p


def create_patient_device(device_type: DeviceType,
                          location: str='test:1',
                          session=None):
    p = PatientDevice(device_type.id, location)
    if session:
        session.add(p)
    return p


def create_nurse_device(device_type: DeviceType,
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


def create_issue(device: PatientDevice, request: RequestType, session=None):
    iss = Issue(device.id, request.id, request.priority)
    if session:
        session.add(iss)
    return iss


class TestPatientHandler(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        from tornado_sqlalchemy import make_session_factory
        APP_ROOT = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../..'))

        options.parse_config_file(
            os.path.join(APP_ROOT, 'config', 'testconfig.py'))
        self.factory = make_session_factory('sqlite:///:memory:')
        app_router = create_router()

        http_server = HTTPServer(
            Dispatcher(
                options,
                app_router,
                session_factory=self.factory))
        http_server.listen(options.port)

        self.instance = IOLoop.instance()
        self.instance.add_callback(IOLoop.instance().stop)
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setup(self):
        raise KeyError()
        self.instance.start()

    def teardown(self):
        raise KeyError()
        self.instance.stop()

    def get_session(self):
        return self.factory.make_session()

    def test_get_issue(self):
        sess = self.get_session()
        patient_type = create_patient_device_type(session=sess)
        request = create_requesttype(patient_type, session=sess)
        dev = create_patient_device(patient_type, session=sess)
        iss = create_issue(dev, request, session=sess)
        param = OrderedDict(
            uuid=dev.id,
            issueid=iss.id,
        )
        sess.commit()
        sess.close()

        url = 'http://localhost:8000/patient/request?' + \
            urllib.parse.urlencode(query=param)
        client = HTTPClient()
        pdb.set_trace()
        response = yield client.fetch(url, method='GET')
        print(response.body)
        self.assertTrue(False is True, msg='fuck')
