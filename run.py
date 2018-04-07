from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import (options,
                             parse_command_line,
                             parse_config_file)
import os
from dispatcher import Dispatcher
from dispatcher import configs


def create_router():
    from dispatcher.patientapi import PatientRouter
    app_router = PatientRouter()
    from dispatcher.nursepanel import NurseRouter
    app_router.append(NurseRouter())
    from dispatcher.adminpanel import AdminRouter
    app_router.append(AdminRouter())
    return app_router


if __name__ == '__main__':
    """Serves as the main entry point to launch the webservice."""
    if options.mode is 'test':
        parse_config_file(os.path.join('.', 'config', 'testconfig.py'))
    else:
        parse_config_file(os.path.join('.', 'config', 'devconfig.py'))
    parse_command_line()

    from tornado_sqlalchemy import make_session_factory
    factory = make_session_factory(options.db)

    # Assemble the tornado application with its submodules
    app_router = None
    try:
        app_router = create_router()
    except KeyError as e:
        print(e)
        exit(1)

    http_server = HTTPServer(
        Dispatcher(
            options,
            app_router,
            session_factory=factory))
    http_server.listen(options.port)

    print('dispatcher is running on localhost:%s' % options.port)

    IOLoop.instance().start()
