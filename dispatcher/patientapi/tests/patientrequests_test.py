from unittest import TestCase
import os
import urllib
from tornado.options import options
from tornado.httpserver import HTTPServer
from tornado.httpclient import HTTPClient
from tornado.ioloop import IOLoop
from dispatcher import Dispatcher
from run import create_router
from collections import OrderedDict


from dispatcher.models import (PatientDevice,
                               PatientDeviceType,
                               RequestType,
                               Issue)
# add application root to sys.path

# convenience method to clear test database
# In this example, we simple reapply APP_ROOT/db/schema.sql to test database

# Create your base Test class.
# Put all of your testing methods here.


# Your TestHandler class
# They are runnable via nosetests as well.
class TestPatientHandler(TestCase):

    def __init__(self, *args, **kwargs):
        from tornado_sqlalchemy import make_session_factory
        APP_ROOT = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../..'))

        options.parse_config_file(
            os.path.join(APP_ROOT, 'config', 'testconfig.py'))

        factory = make_session_factory(options.db)

        # Assemble the tornado application with its submodules
        app_router = None
        try:
            app_router = create_router()
        except KeyError as e:
            print(e)
            exit(1)

        http_server = HTTPServer(
            Dispatcher(
                options,
                app_router,
                session_factory=factory))
        http_server.listen(options.port)

        print('dispatcher is running on localhost:%s' % options.port)

        self.instance = IOLoop.instance()
        self.instance.add_callback(IOLoop.instance().stop)
        TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        print('lol')
        self.instance.start()

    def tearDown(self):
        self.instance.stop()

    def get_session(self):
        return self.factory.make_session()

    def test_get_issue(self):
        dev = None
        iss = None
        sess = self.get_session()
        newpatientdevt = PatientDeviceType('testpdevt',
                                           'used to testing the code')
        sess.add(newpatientdevt)
        # Create new requests for this new device
        pdid = newpatientdevt.id
        newpreq1 = RequestType('ONE',
                               'testone',
                               'used to testing the code',
                               pdid,
                               0)
        newpreq2 = RequestType('TWO',
                               'testtwo',
                               'used to testing the code',
                               pdid,
                               1)
        sess.add(newpreq1)
        sess.add(newpreq2)
        # Create patient device
        dev = PatientDevice(newpatientdevt.id, 'room:501')
        sess.add(dev)
        # Create Issue
        iss = Issue(dev.id, newpreq1.id, newpreq1.priority)
        sess.add(iss)
        # Example on how to hit a particular handler as POST request.
        # In this example, we want to test the redirect,
        # thus follow_redirects is set to False

        param = OrderedDict(
            uuid=dev.id,
            issueid=iss.id,
        )
        url = 'http://localhost:8000/patient/request?' + urllib.parse.urlencode(query=param)
        client = HTTPClient()
        response = yield client.fetch(url)
        self.assertEqual(200, response.code)
        # On successful, response is expected to redirect to /tutoria
