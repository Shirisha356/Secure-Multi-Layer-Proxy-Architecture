
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class UserHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {
            "service": "User Service",
            "status": "running",
            "message": "User API is working"
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

server = HTTPServer(("0.0.0.0", 8000), UserHandler)
print("User service running on port 8000")
server.serve_forever()
