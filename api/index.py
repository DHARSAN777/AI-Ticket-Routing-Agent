from http.server import BaseHTTPRequestHandler
import sys
import os
import json
from urllib.parse import urlparse, parse_qs

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
try:
    from backend.main_simple import app as fastapi_app
except ImportError:
    fastapi_app = None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Health check endpoint
        if self.path == "/api" or self.path == "/api/":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "message": "Ticket Agent API",
                "version": "1.0.0", 
                "status": "running"
            }
            self.wfile.write(json.dumps(response).encode())
            return
            
        # Handle other GET requests
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"message": "POST endpoint working"}
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()