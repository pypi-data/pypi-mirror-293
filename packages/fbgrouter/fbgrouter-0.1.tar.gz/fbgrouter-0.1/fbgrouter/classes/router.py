# classes/router.py

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler, method='GET'):
        method = method.upper()
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = handler

    def dispatch(self, path, method='GET'):
        method = method.upper()
        route = self.routes.get(path, {})
        handler = route.get(method)
        if handler:
            return handler()
        else:
            return "404: Not Found"