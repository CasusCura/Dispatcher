from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin, as_future


class NurseRequestHandler(RequestHandler):
    """docstring for PatientRequestHandler"""
