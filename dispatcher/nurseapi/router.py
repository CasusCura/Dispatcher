from dispatcher import SimpleRouter
from dispatcher.nurseapi import NurseRequestHandler


class NurseRouter(SimpleRouter):
    """docstring for NurseRouter"""
    def __init__(self):
        self.routes = [
            (r'/nurse/request', NurseRequestHandler)
        ]
