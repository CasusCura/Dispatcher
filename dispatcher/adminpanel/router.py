from dispatcher import SimpleRouter
from dispatcher.adminpanel import (PanelHandler,
                                   DeviceHandler,
                                   DevicesHandler,
                                   DeviceTypesHandler)


class AdminRouter(SimpleRouter):
    """docstring for NurseRouter"""
    """docstring for NurseRouter"""
    def __init__(self):
        print(os.getcwd())
        routes = [
            (r'/admin/', PanelHandler),
            (r'/admin/device', DeviceHandler),
            (r'/admin/devices', DevicesHandler),
            (r'/admin/devicetypes', DeviceTypesHandler),
            (r'/admin/(favicon.ico)',
                tornado.web.StaticFileHandler,
                {'path': 'dispatcher/adminpanel/static/'}),
            (r'/admin/images/(.*)',
                tornado.web.StaticFileHandler,
                {'path': 'dispatcher/adminpanel/static/images/'}),
            (r'/admin/fonts/(.*)',
                tornado.web.StaticFileHandler,
                {'path': 'dispatcher/adminpanel/static/fonts/'}),
            (r'/admin/css/(.*)',
                tornado.web.StaticFileHandler,
                {'path': 'dispatcher/adminpanel/static/css/'}),
            (r'/admin/js/(.*)',
                tornado.web.StaticFileHandler,
                {'path': 'dispatcher/adminpanel/static/js/'})
        ]
        super(AdminRouter, self).__init__(routes)
