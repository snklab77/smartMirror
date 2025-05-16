# /usr/local/bin/smartmirror_server.py
import http.server
import socketserver
import os

PORT = 8000
# Set the document root to your smart mirror directory
DOCROOT = "/home/[your username]/smartMirror"

os.chdir(DOCROOT)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving {DOCROOT} at http://localhost:{PORT}")
    httpd.serve_forever()