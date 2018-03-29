from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from dispatcher.models import (NurseDevice,
                               Response,
                               IssueStates)
import json


class NurseVerificationHandler(RequestHandler, SessionMixin):
    def post(self):
        data = json.loads(self.request.body)
        ret = None
        uuid = None
        try:
            uuid = data['uuid']
        except KeyError as ke:
            ret = {
                'success': False,
                'code': 400,
                'error': 'UUID Not provided',
                'status': 'BAD'
            }
        if uuid:
            with self.make_session() as session:
                device = session.query(NurseDevice)\
                    .filter(NurseDevice.id == uuid.encode())\
                    .first()
                if device:
                    ret = {
                        'success': True,
                        'code': 200,
                        'status': 'OK'
                    }
                else:
                    ret = {
                        'success': False,
                        'code': 400,
                        'status': 'BAD'
                    }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()


class MyIssuesHandler(RequestHandler, SessionMixin):
    def get(self):
        uuid = self.get_argument('uuid', None)
        if uuid:
            with self.make_session() as session:
                queued_issues = session.query(Response)\
                    .filter(Response.nursedevice == uuid.encode(),
                            Response.issue.status == IssueStates.QUEUED)\
                    .all()
                pending_issues = session.query(Response)\
                    .filter(Response.issue.status == IssueStates.PENDING)\
                    .all()
                queued_issues_json = [qi.serialize() for qi in queued_issues]
                pending_issues_json = [pi.serialize() for pi in pending_issues]
                ret = {
                    'code': 200,
                    'status': 'OK',
                    'pending_issues': pending_issues_json,
                    'queued_issues': queued_issues_json,
                }
        else:
            ret = {
                'code': 400,
                'status': 'BAD'
            }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()


class ResponseHandler(RequestHandler, SessionMixin):
    def post(self):
        data = json.loads(self.request.body)
        ret = None
        response = None
        try:
            response = data['response']
        except KeyError as ke:
            ret = {
                'success': False,
                'code': 400,
                'error': 'UUID Not provided',
                'status': 'BAD'
            }


class CloseIssueHandler(RequestHandler, SessionMixin):
    def post(self):
        return
