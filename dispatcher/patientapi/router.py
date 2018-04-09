from dispatcher import SimpleRouter
from dispatcher.patientapi import (PatientRequestHandler,
                                   PatientRequest1Handler,
                                   PatientTestHandler)


class PatientRouter(SimpleRouter):
    """docstring for PatientRouter"""
    def __init__(self):
        self.routes = [
            (r'/patient/request', PatientRequestHandler),
            (r'/patient/request1', PatientRequest1Handler),
            #(r'/patient/request/delete', PatientDeleteHandler),
            (r'/patient/test', PatientTestHandler),
        ]
