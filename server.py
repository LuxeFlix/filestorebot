import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        # Back4App-কে রেসপন্স পাঠাবে
        self.wfile.write(b"Telegram Bot is alive and running with 0 RAM!")

    # 🚀 Logs-এ অপ্রয়োজনীয় পিং মেসেজ অফ করার জন্য
    def log_message(self, format, *args):
        pass

def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()
