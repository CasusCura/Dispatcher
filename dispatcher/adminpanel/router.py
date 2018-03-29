from dispatcher import SimpleRouter
from dispatcher.adminpanel import (PanelHandler,
                                   NursePanelHandler,
                                   DeviceHandler,
                                   DevicesHandler,
                                   DeviceTypeHandler,
                                   RequestTypeHandler,
                                   RequestTypesHandler,
                                   DeviceTypesHandler)

import tornado


class AdminRouter(SimpleRouter):
    """Docstring for AdminRouter."""
    def __init__(self):
        routes = [
            (r'/admin/', PanelHandler),
            (r'/admin/nurse/', NursePanelHandler),
            (r'/admin/device', DeviceHandler),
            (r'/admin/devices', DevicesHandler),
            (r'/admin/devicetype', DeviceTypeHandler),
            (r'/admin/devicetypes', DeviceTypesHandler),
            (r'/admin/requesttype', RequestTypeHandler),
            (r'/admin/requesttypes', RequestTypesHandler),
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
