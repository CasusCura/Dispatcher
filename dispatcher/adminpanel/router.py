from dispatcher import SimpleRouter
from dispatcher.adminpanel import adminpanelRequestHandler


class AdminRouter(SimpleRouter):
    """docstring for NurseRouter"""
    def __init__(self):
        routes = [
            (r'/admin/request', adminpanelRequestHandler)
        ]
        super(AdminRouter, self).__init__(routes)
