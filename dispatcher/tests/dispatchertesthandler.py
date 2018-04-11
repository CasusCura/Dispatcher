from tornado_sqlalchemy import make_session_factory
from dispatcher.adminpanel import AdminRouter
from dispatcher.patientapi import PatientRouter
from dispatcher.nursepanel import NurseRouter
from dispatcher import Dispatcher
from testnado import HandlerTestCase


class DispatcherTestHandler(HandlerTestCase):

    def get_app(self):
        app_router = PatientRouter()
        app_router.append(NurseRouter())
        app_router.append(AdminRouter())
        return Dispatcher(None, app_router, self.factory)

    def setUp(self):
        self.factory = make_session_factory('sqlite:///./test.db')
        super(DispatcherTestHandler, self).setUp()
        self.classes = set()
        self.session = self.factory.make_session()

    def tearDown(self):
        super(DispatcherTestHandler, self).tearDown()
        self.session = self.factory.make_session()
        for cls in self.classes:
            self.query(cls).delete()
        self.commit()

    def query(self, cls):
        return self.session.query(cls)

    def commit(self):
        self.session.commit()
        self.session.close()

    def add(self, *obj):
        for o in obj:
            self.classes.add(type(o))
            self.session.add(o)

    def delete(self, *obj):
        for o in obj:
            self.session.delete(o)
