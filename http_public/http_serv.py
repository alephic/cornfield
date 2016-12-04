from http.server import *
import shutil

def run():
  server_address = ('', 8000)
  httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
  httpd.serve_forever()
