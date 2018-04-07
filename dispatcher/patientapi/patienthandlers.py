from tornado.web import RequestHandler
from dispatcher.models import (Issue,
                               IssueStates,
                               Device,
                               RequestType,
                               RequestData)
from tornado_sqlalchemy import SessionMixin
import json

# TODO: Verify that data is valid JSON/dict
# TODO: Verify that uuid is a 32 character string
# TODO: Verify that request id is a string


class PatientRequestHandler(RequestHandler, SessionMixin):
    """docstring for PatientRequestHandler"""
    def get(self):
        """Returns information for the current issue associated with this
        device."""
        print('HEHE')
        # TODO: Validate uuid
        uuid = self.get_argument('uuid')
        ret = self._get(uuid)
        if ret['issue']:
            self.set_status(200)
            self.write(json.dump(ret))
        else:
            self.set_status(400)
            self.write(json.dump(ret))
        self.finish()

    def _get(self, uuid):
        issue = None
        with self.make_session() as session:
            issue = session.query(Issue)\
                .filter(Issue.patientdevice == uuid,
                        Issue.status < 3)\
                .first()
        if issue:
            return {
                'status': 'OK',
                'issue': issue.as_json(),
                'code': 200,
            }
        return {
            'status': 'BAD',
            'issue': None,
            'code': 400,
        }

    def post(self):
        """Creates a new issue for this patient device."""
        # Get Variables
        data = json.loads(self.request.body)
        request_id = None
        r_data = None
        uuid = None
        ret = None
        try:
            uuid = data['device_id']
            request_id = data['request_id']
            r_data = data['data']
        except KeyError as ke:
            ret = {
                'status': 'BAD',
                'issue': None,
                'code': 400,
            }
        print(uuid, request_id, r_data)
        # Verify Valid parameters
        if uuid and request_id:
            ret = self._post(uuid, request_id, r_data)
        self.write(ret)
        self.set_status(ret['code'])
        self.finish()

    def _post(self, device_id, request_id, request_data):
        device = None
        request_type = None
        issue = None
        with self.make_session() as session:
            device = session.query(Device)\
                .filter(Device.id == device_id.encode())\
                .first()
            print(device)
            request_type = session.query(RequestType)\
                .filter(RequestType.devicetype == device.devicetype)\
                .all()
            print([t.serialize() for t in request_type])
        # Handle invalid rid
            if len(request_type) != 1:
                return {'status': 'BAD', 'code': 400}
            request_type = request_type[0]
            # Create Issue
            issue = Issue(device_id, request_type.id, request_type.priority)
            session.add(issue)
            if request_data:
                requestdata = RequestData(device_id, issue.id,
                                          json.load(request_data))
                session.add(requestdata)
            if issue:
                return {'status': 'OK', 'issueid': str(issue.id)[2:-1],'code': 200 }
            else:
                return {'status': 'BAD', 'error': 'nothing found', 'code': 400}

    def update(self):
        """Adds request data or updates repeated issue."""
        uuid = self.get_argument('uuid')
        issue_id = self.get_argument('issueid')
        data = self.get_argument('data')
        with self.make_session() as session:
            q_issue = session.query(Issue)\
                .filter(Issue.patientdevice == uuid,
                        Issue.status < 3,
                        Issue.id == issue_id)
            if len(q_issue.all()) == 0:
                self.set_status(400)
            elif len(q_issue.all()) >= 1:
                issue = q_issue.first()
                if data:
                    requestdata = RequestData(uuid, issue.id, json.load(data))
                    session.add(requestdata)
                    self.set_status(201)
                else:
                    self.set_status(400)
            else:
                self.set_status(500)
        self.finish()


class PatientRequest1Handler(RequestHandler, SessionMixin):

    def post(self):
        """Creates a new issue for this patient device."""
        # Get Variables
        data = str(self.request.body)
        tokens = data.split('&')
        uuid = tokens[0].split('=')[1].replace('-', '')
        request_id = tokens[1].split('=')[1][:-1]
        r_data = {}
        #request_id = None
        #r_data = None
        #uuid = None
        ret = None
        #try:
        #    uuid_uuid = self.get_argument('device_id')
        #    uuid = uuid_uuid.replace('-', '')
        #    request_id = self.get_argument('request_id')
        #    r_data = {}
        #except KeyError as ke:
        #    ret = {
        #        'status': 'BAD',
        #        'issue': None,
        #        'code': 400,
        #    }
        print(uuid, request_id, r_data)
        # Verify Valiparameters
        ret = self._post(uuid, request_id, r_data)
        self.write(ret)
        self.set_status(ret['code'])
        self.finish()

    def _post(self, device_id, request_id, request_data):
        device = None
        request_type = None
        issue = None
        with self.make_session() as session:
            device = session.query(Device)\
                .filter(Device.id == device_id.encode())\
                .first()
            print(device)
            if device:
                request_type = session.query(RequestType)\
                    .filter(RequestType.devicetype == device.devicetype)\
                    .all()
                print([t.serialize() for t in request_type])
            # Handle invalid rid
                if len(request_type) != 1:
                    return {'status': 'BAD', 'code': 400}
                request_type = request_type[0]
                # Create Issue
                issue = Issue(device_id, request_type.id, request_type.priority)
                session.add(issue)
                if request_data:
                    requestdata = RequestData(device_id, issue.id,
                                              json.load(request_data))
                    session.add(requestdata)
                if issue:
                    return {'status': 'OK', 'issueid': str(issue.id)[2:-1],'code': 200 }
                else:
                    return {'status': 'BAD', 'error': 'nothing found', 'code': 400}



class PatientTestHandler(RequestHandler, SessionMixin):
    def get(self):
        self.set_status(200)
        self.finish()


class PatientDeleteHandler(RequestHandler, SessionMixin):
    def post(self):
        """Cancels the active issue for this device."""
        uuid = self.get_argument('uuid')
        issueid = self.get_argument('issueid')
        with self.make_session() as session:
            q_issue = session.query(Issue)\
                .filter(Issue.id == issueid,
                        Issue.patientdevice == uuid,
                        Issue.status < 3)
            if len(q_issue.all()) != 1:
                self.set_status(400)
                self.write(json.dump({'status': 'DENIED', }))
                self.finish()
                return
            issue = q_issue.first()
            issue.status = IssueStates.CANCELLED
            self.set_status(200)
            self.write(json.dump({'status': 'OK', }))
        self.finish()
        return
