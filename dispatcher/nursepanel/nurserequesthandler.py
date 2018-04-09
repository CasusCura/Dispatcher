from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from dispatcher.models import (NurseDevice,
                               Response,
                               IssueStates,
                               Issue)
import json


class PanelHandler(RequestHandler, SessionMixin):
    def get(self):
        """Render the panel."""
        self.render('static/index.html')


class NurseVerificationHandler(RequestHandler, SessionMixin):
    def post(self):
        print(self.request.body)
        ret = None
        uuid = None
        try:
            data = json.loads(self.request.body)
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


class IssuesHandler(RequestHandler, SessionMixin):
    def get(self):
        uuid = self.get_argument('uuid', None)
        print(self.request)
        print('uuid', uuid)
        if uuid:
            with self.make_session() as session:
                active_issues = session.query(Issue)\
                    .filter(Issue.status == IssueStates.QUEUED)\
                    .all()
                my_active_issues = []
                other_active_issues = []
                for issue in active_issues:
                    responses = session.query(Response)\
                        .filter(Response.issueid == issue.id)\
                        .all()
                    for response in responses:
                        print(response.nursedevice, uuid)
                        if response.nursedevice == uuid:
                            my_active_issues.append(issue)
                        else:
                            other_active_issues.append(issue)
                pending_issues = session.query(Issue)\
                    .filter(Issue.status == IssueStates.PENDING)\
                    .all()
                my_queued_issues_json = [qi.serialize()
                                         for qi
                                         in my_active_issues]
                other_queued_issues_json = [qi.serialize()
                                            for qi
                                            in other_active_issues]
                pending_issues_json = [pi.serialize()
                                       for pi
                                       in pending_issues]
                ret = {
                    'code': 200,
                    'status': 'OK',
                    'pending_issues': pending_issues_json,
                    'my_queued_issues': my_queued_issues_json,
                    'other_queued_issues': other_queued_issues_json,
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
                'code': 400,
                'error': 'UUID Not provided',
                'status': 'BAD'
            }
        if response:
            ret = self._post(response)
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _post(self, params):
        with self.make_session() as session:
            issue = session.query(Issue)\
                .filter(Issue.id == params['issue_id'].encode())\
                .first()
            response = Response(
                    issueid=issue.id,
                    eta=params['eta'],
                    nursedeviceid=params['nurse_id'],
                    data=params['data']
            )
            session.add(response)
            issue.status = IssueStates.QUEUED
            if response:
                return {
                    'code': 200,
                    'status': 'OK',
                    'response_id': str(response.id)[2:-1]
                }
            else:
                return {
                    'code': 400,
                    'error': 'Could not create response',
                    'status': 'BAD'
                }


class CloseIssueHandler(RequestHandler, SessionMixin):
    def post(self):
        print(self.request.body)
        data = json.loads(self.request.body)
        issue_id = None
        nurse_id = None
        try:
            issue_id = data['issue_id']
            nurse_id = data['nurse_id']
        except KeyError as ke:
            ret = {
                'code': 400,
                'error': 'Missing both parameters',
                'status': 'BAD'
            }
        if nurse_id and issue_id:
            ret = self._post(issue_id, nurse_id)
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _post(self, issue_id, nurse_id):
        with self.make_session() as session:
            issue = session.query(Issue)\
                .filter(Issue.id == issue_id.encode())\
                .first()
            issue.status = IssueStates.CLOSED
            return {
                'code': 200,
                'status': 'ok'
            }
