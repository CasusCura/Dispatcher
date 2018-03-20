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
        uuid = self.get_argument('uuid')
        with self.make_session() as session:
            q_issue = session.query(Issue).filter(Issue.patientdevice == uuid)
            if len(q_issue.all()) == 0:
                self.set_status(200)
                self.finish()
                return
            elif len(q_issue.all()) >= 1:
                self.writeout(q_issue.first().id)
                self.set_status(200)
            else:
                self.set_status(500)
        self.finish()

    def post(self):
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

    def create(self):
        """Creates a new issue for this patient device."""
        # Get Variables
        uuid = self.get_argument('uuid')
        request_id = self.get_argument('rid')
        data = self.get_argument('data')
        # Verify Valid parameters
        with self.make_session() as session:
            q_device = session.query(Device)\
                .filter(Device.patientdevice == uuid)
            # Handle invalid uuid
            if len(q_device.all()) != 1:
                self.set_status(401)
                self.finish()
                return
            device_type_id = q_device.first().devicetype.id
            q_request_type = session.query(RequestType)\
                .filter(RequestType.devicetype == device_type_id,
                        RequestType.device_request_id == request_id)
            # Handle invalid rid
            if len(q_request_type.all()) != 1:
                self.set_status(401)
                self.finish()
                return
            request_type = q_request_type.first()
            # Create Issue
            issue = Issue(uuid, request_type.id, request_type.priority)
            session.add(issue)
            if data:
                requestdata = RequestData(uuid, issue.id, json.load(data))
                session.add(requestdata)
            self.writeout(json.dump({'status': 'OK', 'issueid': issue.id, }))
        self.set_status(201)
        self.finish()

    def delete(self):
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
                self.writeout(json.dump({'status': 'DENIED', }))
                self.finish()
                return
            issue = q_issue.first()
            issue.status = IssueStates.CANCELLED
            self.set_status(202)
            self.writeout(json.dump({'status': 'OK', }))
        self.finish()
        return

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


class PatientTestHandler(RequestHandler, SessionMixin):
    def get(self):
        self.set_status(200)
        self.finish()
