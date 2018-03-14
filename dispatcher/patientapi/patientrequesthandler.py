from tornado.web import RequestHandler


class PatientRequestHandler(RequestHandler):
    """docstring for PatientRequestHandler"""
    def get(self):
        self.clear()
        self.set_status(501)
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
