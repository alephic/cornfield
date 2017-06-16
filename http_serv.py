from http.server import *
import os

os.chdir('http_public/')
server_address = ('', 8000)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
httpd.serve_forever()
