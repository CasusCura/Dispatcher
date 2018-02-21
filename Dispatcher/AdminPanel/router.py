from Dispatcher import SimpleRouter
from Dispatcher.AdminPanel import AdminPanelRequestHandler


class AdminRouter(SimpleRouter):
    """docstring for NurseRouter"""
    def __init__(self):
        routes = [
            (r'/admin/request', AdminPanelRequestHandler)
        ]
        super(AdminRouter, self).__init__(routes)
