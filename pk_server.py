from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial

hostName = "localhost"
serverPort = 8080


class pkHandler(BaseHTTPRequestHandler):
  def __init__(self, db, *args, **kwargs):
    self.db = db
    super().__init__(*args, **kwargs)

  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

    if self.path is '/':
      fp = open("PokeRater-test.html", "r")
      self.wfile.write(bytes(fp.read(), "utf-8"))
    else:
      # TODO: get pokemon info
      path, options = self.path.split('?')
      path = path.split('/')
      print(path)
      self.wfile.write(bytes("ditto", "utf-8"))

  def do_POST(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    # <--- Gets the size of data
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)  # <--- Gets the data itself
    print(post_data)

    #format: b'{"shuffle":false,"rating":"4.5"}'

    # DEBUG: info
    message = "Hello, World! Here is a POST response"
    self.wfile.write(bytes(message, "utf8"))


class pkServer:
  def __init__(self, db, host, port):
    self.handler = partial(pkHandler, db)
    self.server = HTTPServer((host, port), self.handler)

  def run(self):
    try:
      self.server.serve_forever()
    except KeyboardInterrupt:
      pass

    self.server.server_close()
