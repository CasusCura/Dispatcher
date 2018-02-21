"""Object that stores the routes for packages of this webapp. Looking into
any router object of a module will give you a over view of the urls and
end points associated with a module."""

from typing import List, Tuple
from tornado.web import RequestHandler

Route_list = List[Tuple[str, RequestHandler]]


class SimpleRouter(object):
    """Holds all URL endpoints and associated handler objects for the current
    module of the dispatcher."""

    def __init__(self, routes: Route_list):
        self._routes = routes

    def append(self, router) -> bool:
        """Appends a router to self if the router doesn't have any duplicate
        endpoints. If there its a duplicate a KeyError is raised."""
        urls = [route[0] for route in self._routes]

        try:
            for route in router._routes:
                if route[0] in urls:
                    raise KeyError('Urls endpoint Already defined')
            self._routes = self._routes + router._routes
            return True
        except KeyError:
            pass
