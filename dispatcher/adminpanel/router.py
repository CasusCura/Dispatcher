from dispatcher import SimpleRouter
from dispatcher.adminpanel import (PanelHandler,
                                   DeviceHandler,
                                   DevicesHandler,
                                   DeviceTypesHandler)


class AdminRouter(SimpleRouter):
    """docstring for NurseRouter"""
    def __init__(self):
        routes = [
            (r'/admin/', PanelHandler),
            (r'/admin/device', DeviceHandler),
            (r'/admin/devices', DevicesHandler),
            (r'/admin/devicetypes', DeviceTypesHandler),
        ]
        super(AdminRouter, self).__init__(routes)
