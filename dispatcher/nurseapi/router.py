from dispatcher import SimpleRouter
from dispatcher.nurseapi import (NurseVerificationHandler,
                                 MyIssuesHandler,
                                 ResponseHandler,
                                 CloseIssueHandler)


class NurseRouter(SimpleRouter):
    """docstring for NurseRouter"""
    def __init__(self):
        self.routes = [
            (r'/nurse/login', NurseVerificationHandler),
            (r'/nurse/myissues', MyIssuesHandler),  # I have many
            (r'/nurse/response', ResponseHandler),
            (r'/nurse/close', CloseIssueHandler),
        ]
