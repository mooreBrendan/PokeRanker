from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
import json

hostName = "localhost"
serverPort = 8080


class pkHandler(BaseHTTPRequestHandler):
  def __init__(self, db, *args, **kwargs):
    self.db = db
    super().__init__(*args, **kwargs)

  def do_GET(self):
    if "/resources" in self.path:
      self.send_response(200)
      self.send_header("Content-type", "image/png")
      self.end_headers()
      fp = open("."+self.path, "rb")
      self.wfile.write(fp.read())
      return

    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

    print(self.path)
    if self.path == '/':
      fp = open("PokeRater.html", "r")
      self.wfile.write(bytes(fp.read(), "utf-8"))
      return
    elif self.path == "/first":
      print("first")
      next_id = self.db.get_next_sequential(0)
      pk_info = self.db.get_pokemon_by_id(next_id)
    elif self.path == "/rand":
      print("rand")
      next_id = self.db.get_next_rand()
      pk_info = self.db.get_pokemon_by_id(next_id)
    elif '?' in self.path:  # sequential
      path, options = self.path.split('?')
      print(f"{path=}")
      print(options)
      pk_id = self.db.get_id_by_name(options)
      next_id = self.db.get_next_sequential(pk_id)
      pk_info = self.db.get_pokemon_by_id(next_id)
    else:
      print("else")
      pk_info = self.db.get_pokemon_by_name(self.path[1:])
    # print(pk_info)
    # urls = ','.join(pk_info[1])
    # pk_info = str(pk_info[0]) + '[' + urls + ']'
    generations = self.db.get_generations()
    gens = "["
    for gen in generations:
      avg = self.db.get_average(gen)
      rem = len(self.db.get_unrated_gen_ids(gen))
      gens += "["+str(gen)+','+str(avg)+","+str(rem)+"]"
      if gen != generations[-1]:
        gens += ","
    gens += "]"
    print(gens)
    pk_data = '{"name":"'+pk_info[0]+'","urls":'+pk_info[1]+',"gens":'+gens+'}'
    print(pk_data)

    self.wfile.write(bytes(pk_data, "utf-8"))

  def do_POST(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    # <--- Gets the size of data
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)  # <--- Gets the data itself
    post_data = json.loads(post_data.decode("utf-8"))
    self.db.set_rating(post_data["name"], float(post_data["rating"]))
    print(post_data)

    #format: b'{"shuffle":false,"rating":"4.5"}'

    # DEBUG: info
    message = "submitted"
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
