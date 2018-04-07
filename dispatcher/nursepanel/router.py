from dispatcher import SimpleRouter
from dispatcher.nursepanel import (PanelHandler,
                                 NurseVerificationHandler,
                                 MyIssuesHandler,
                                 ResponseHandler,
                                 CloseIssueHandler)

import tornado


class NurseRouter(SimpleRouter):
    """docstring for NurseRouter"""
    def __init__(self):
        self.routes = [
            (r'/nurse/', PanelHandler),
            (r'/nurse/login', NurseVerificationHandler),
            (r'/nurse/myissues', MyIssuesHandler),  # I have many
            (r'/nurse/response', ResponseHandler),
            (r'/nurse/close', CloseIssueHandler),
            (r'/nurse/(favicon.ico)',
                tornado.web.StaticFileHandler,
                {'path': 'dispatcher/nursepanel/static/'}),
            (r'/nurse/resources/(.*)',
                tornado.web.StaticFileHandler,
                {'path': 'dispatcher/nursepanel/static/resources/'}),
        ]
