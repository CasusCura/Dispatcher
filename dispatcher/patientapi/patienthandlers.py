from tornado.web import RequestHandler
from dispatcher.models import (Issue,
                               IssueStates,
                               Device,
                               RequestType,
                               RequestData)
from tornado_sqlalchemy import SessionMixin
from sqlalchemy import or_
import json

# TODO: Verify that data is valid JSON/dict
# TODO: Verify that uuid is a 32 character string
# TODO: Verify that request id is a string


class PatientRequestHandler(RequestHandler, SessionMixin):
    """docstring for PatientRequestHandler"""
    def get(self):
        """Returns information for the current issue associated with this
        device."""
        # TODO: Validate uuid
        uuid = self.get_argument('device_id')
        uuid = uuid.replace('-', '')
        print(uuid)
        ret = self._get(uuid)
        if ret['issue']:
            self.set_status(200)
            self.write(json.dumps(ret))
        else:
            self.set_status(400)
            self.write(json.dumps(ret))
        self.finish()

    def _get(self, uuid):
        issue = None
        with self.make_session() as session:
            issue = session.query(Issue)\
                .filter(Issue.patientdevice == uuid.encode())\
                .order_by(Issue.first_issued.desc())\
                .first()
            if issue:
                return {
                    'status': 'OK',
                    'issue': issue.serialize(),
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

        ret = None

        uuid = data.pop('device_id', None)
        request_id = data.pop('request_id', None)
        issue_id = data.pop('issue_id', None)
        r_data = data.pop('data', None)

        print(uuid, request_id, r_data)
        # Verify Valid parameters
        if uuid and request_id and not issue_id:
            ret = self._post(uuid, request_id, r_data)
        elif uuid and issue_id:
            ret = self._update(uuid, issue_id, r_data)
        else:
            ret = {
                'code': 400,
                'status': 'BAD',
            }

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
                return {
                    'status': 'BAD',
                    'code': 400
                }
            request_type = request_type[0]
            # Create Issue
            issue = Issue(device_id, request_type.id, request_type.priority)
            session.add(issue)
            if request_data:
                requestdata = RequestData(device_id,
                                          issue.id,
                                          json.loads(request_data))
                session.add(requestdata)
            if issue:
                return {
                    'status': 'OK',
                    'issue_id': str(issue.id)[2:-1],
                    'code': 200,
                }
            else:
                return {
                    'status': 'BAD',
                    'error': 'nothing found',
                    'code': 400
                }

    def _update(self, uuid, issue_id, data):
        """Adds request data or updates repeated issue."""
        ret = None
        print(uuid, issue_id, data)
        with self.make_session() as session:
            q_issue = session.query(Issue)\
                .filter(Issue.id == issue_id.encode(),
                        Issue.patientdevice == uuid.encode())
            print([i.serialize() for i in session.query(Issue).all()])
            print(q_issue.all())
            if len(q_issue.all()) == 0:
                ret = {
                    'code': 400,
                    'error': 'No issue found.',
                }
            elif len(q_issue.all()) >= 1:
                issue = q_issue.first()
                if data:
                    requestdata = RequestData(uuid, issue.id, json.loads(data))
                    session.add(requestdata)
                    ret = {
                        'code': 201,
                        'status': 'ok',
                    }
                else:
                    ret = {
                        'code': 400,
                        'error': 'No data supplied.',
                    }
            else:
                ret = {
                    'code': 500,
                    'error': 'Serv Err',
                }
        return ret

    def delete(self):
        """Cancels the active issue for this device."""
        uuid = self.get_argument('device_id')
        with self.make_session() as session:
            q_issue = session.query(Issue)\
                .filter(Issue.patientdevice == uuid.encode(),
                        or_(Issue.status == IssueStates.QUEUED,
                            Issue.status == IssueStates.PENDING))

            if len(q_issue.all()) != 1:
                self.set_status(400)
                self.write(json.dumps({'status': 'DENIED', }))
                self.finish()
                return
            issue = q_issue.first()
            issue.status = IssueStates.CANCELLED
            self.set_status(200)
            self.write(json.dumps({'status': 'OK', }))
        self.finish()
        return


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
                    return {'status': 'OK', 'issue_id': str(issue.id)[2:-1],'code': 200 }
                else:
                    return {'status': 'BAD', 'error': 'nothing found', 'code': 400}


class PatientDeleteHandler(RequestHandler, SessionMixin):
    def post(self):
        """Cancels the active issue for this device."""
        print(self.request.body)
        data = json.loads(self.request.body)
        print(data)
        uuid = data.pop('device_id', None)
        issue_id = data.pop('issue_id', None)
        print(uuid)
        with self.make_session() as session:
            q_issue = session.query(Issue)\
                .filter(Issue.patientdevice == uuid.encode(),
                        or_(Issue.status == IssueStates.QUEUED,
                            Issue.status == IssueStates.PENDING))

            if len(q_issue.all()) != 1:
                self.set_status(400)
                self.write(json.dumps({'status': 'DENIED', }))
                self.finish()
                return
            issue = q_issue.first()
            issue.status = IssueStates.CANCELLED
            self.set_status(200)
            self.write(json.dumps({'status': 'OK', }))
        self.finish()
        return



class PatientTestHandler(RequestHandler, SessionMixin):
    def get(self):
        self.set_status(200)
        self.finish()
