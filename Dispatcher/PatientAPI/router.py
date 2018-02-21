from dispatcher import SimpleRouter
from dispatcher.patientapi import PatientRequestHandler


class PatientRouter(SimpleRouter):
    """docstring for PatientRouter"""
    def __init__(self):
        routes = [
            (r'/patient/request', PatientRequestHandler)
        ]
        super(PatientRouter, self).__init__(routes)
