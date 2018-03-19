"""Main dispatcher application code which defines """
from tornado.web import Application
from dispatcher import SimpleRouter


class Dispatcher(Application):
    """dispatcher tornado application object. Used for creating the dispatcher
    instance. """
    debug = True

    def __init__(self, command_options, router: SimpleRouter):
        self.options = command_options

        super(Dispatcher, self).__init__(
            router._routes,
            debug=self.debug
        )