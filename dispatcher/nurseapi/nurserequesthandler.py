from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin, as_future


class NurseRequestHandler(RequestHandler):
    """docstring for PatientRequestHandler"""
    def get(self):
        self.clear()
        self.set_status(200)
        self.finish("""<html><body>Not the endpoint you were looking for
        </body></html>""")

    def post(self):
        self.clear()
        self.set_status(501)
        self.finish("""<html><body>Not the endpoint you were looking for
        </body></html>""")

    def delete(self):
        self.clear()
        self.set_status(501)
        self.finish("""<html><body>Not the endpoint you were looking for
        </body></html>""")

    def update(self):
        self.clear()
        self.set_status(501)
        self.finish("""<html><body>Not the endpoint you were looking for
        </body></html>""")
