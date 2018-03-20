from dispatcher import SimpleRouter
from dispatcher.patientapi import PatientRequestHandler, PatientTestHandler


class PatientRouter(SimpleRouter):
    """docstring for PatientRouter"""
    def __init__(self):
        self.routes = [
            (r'/patient/request', PatientRequestHandler),
            (r'/patient/test', PatientTestHandler)
        ]
