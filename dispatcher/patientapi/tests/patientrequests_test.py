import unittest
import json
import urllib
from dispatcher.tests import DispatcherTestHandler
from testnado.credentials import HeaderCredentials


from dispatcher.models import (Device,
                               DeviceType,
                               PatientDevice,
                               PatientDeviceType,
                               NurseDevice,
                               NurseDeviceType,
                               Response,
                               RequestType,
                               Issue,
                               ModelCreationMixin)


class TestPatientHandler(DispatcherTestHandler,
                         ModelCreationMixin):
    def get_credentials(self):
        # return a credentials object that updates a
        # response object with the proper stuff
        return HeaderCredentials({"X-Auth-Token": 'placeholder'})

    def test_get_issue(self):
        patient_type = self.create_patient_device_type(session=self)
        request = self.create_requesttype(patient_type, session=self)
        dev = self.create_patient_device(patient_type, session=self)
        iss = self.create_issue(dev, request, session=self)
        device_id = dev.id.decode('utf-8')
        issue_id = iss.id.decode('utf-8')
        self.commit()
        params = {
            'device_id': device_id
        }
        path = '/patient/request?' + urllib.parse.urlencode(params)

        response = self.authenticated_fetch(path, 'GET')
        string = response.buffer.read().decode('utf-8')
        results = json.loads(string)
        self.assertEqual(issue_id, results['issue']['id'])


if __name__ == '__main__':
    unittest.main()
