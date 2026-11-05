from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class OrderHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {
            "service": "Order Service",
            "status": "running",
            "message": "Order API is working"
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

server = HTTPServer(("0.0.0.0", 8000), OrderHandler)
print("Order service running on port 8000")
server.serve_forever()
