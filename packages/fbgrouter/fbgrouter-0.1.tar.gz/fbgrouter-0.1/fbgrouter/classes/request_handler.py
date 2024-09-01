# classes/request_handler.py
from http.server import BaseHTTPRequestHandler
from routes.web import router


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = router.dispatch(self.path, method='GET')
        self.send_response(200 if "404" not in response else 404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        response = router.dispatch(self.path, method='POST')
        self.send_response(200 if "404" not in response else 404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def do_PUT(self):
        response = router.dispatch(self.path, method='PUT')
        self.send_response(200 if "404" not in response else 404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def do_DELETE(self):
        response = router.dispatch(self.path, method='DELETE')
        self.send_response(200 if "404" not in response else 404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))