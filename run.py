from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from dispatcher import dispatcher


# Define command line parameters
define("port", default=8888, help="run on the given port", type=int)
define("db",
       default="sqlite://dispatcher-0.1.db",
       help="run with the given database file",
       type=str)


if __name__ == '__main__':
    """Serves as the main entry point to launch the webservice."""
    parse_command_line()

    from tornado_sqlalchemy import make_session_factory
    factory = make_session_factory(options.db)

    # Assemble the tornado application with its submodules
    app_router = None
    try:
        from dispatcher.patientapi import PatientRouter
        app_router = PatientRouter()
        from dispatcher.nurseapi import NurseRouter
        app_router.append(NurseRouter())
        from dispatcher.adminpanel import AdminRouter
        app_router.append(AdminRouter())

    except KeyError as e:
        print(e)
        exit(1)

    http_server = HTTPServer(dispatcher(options, app_router))
    http_server.listen(options.port)

    print('dispatcher is running on localhost:%s' % options.port)

    IOLoop.instance().start()
