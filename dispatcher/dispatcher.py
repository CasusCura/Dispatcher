"""Main dispatcher application code which defines """
from tornado.web import Application
from dispatcher import SimpleRouter


class Dispatcher(Application):
    """dispatcher tornado application object. Used for creating the dispatcher
    instance."""

    def __init__(self, command_options, router: SimpleRouter,
                 session_factory, debug=False):
        self.options = command_options
        self.debug = debug
        from dispatcher.database import init_db
        init_db(session_factory)
        super(Dispatcher, self).__init__(
            router.routes,
            debug=self.debug,
            session_factory=session_factory
        )
