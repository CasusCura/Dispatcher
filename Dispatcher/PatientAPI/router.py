from Dispatcher import SimpleRouter
from Dispatcher.PatientAPI import PatientRequestHandler


class PatientRouter(SimpleRouter):
    """docstring for PatientRouter"""
    def __init__(self):
        routes = [
            (r'/patient/request', PatientRequestHandler)
        ]
        super(PatientRouter, self).__init__(routes)
