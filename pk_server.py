from http.server import BaseHTTPRequestHandler, HTTPServer


hostName = "localhost"
serverPort = 8080


class pkServer(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    if self.path == '/':
      fp = open("PokeRater-test.html", "r")
      self.wfile.write(bytes(fp.read(), "utf-8"))
    else:
      # TODO: get pokemon info
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


class pkServerManager:
  def __init__(self, db, host, port):
    self.db = db
    self.server = HTTPServer((host, port), pkServer)

  def run(self):
    try:
      self.server.serve_forever()
    except KeyboardInterrupt:
      pass

    self.server.server_close()
