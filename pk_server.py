"""Server for the webpage"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
import json


class PKHandler(BaseHTTPRequestHandler):
  """handles web requests"""

  def __init__(self, db, *args, **kwargs):
    """initializes the hanlder for the website
    Args: db (DB object): the database for the project"""
    self.db = db
    super().__init__(*args, **kwargs)

  def do_GET(self):
    """handles GET requests"""

    # check and send images
    if "/resources" in self.path:
      self.send_response(200)
      self.send_header("Content-type", "image/png")
      self.end_headers()
      fp = open("."+self.path, "rb")
      self.wfile.write(fp.read())
      return

    # send text information otherwise
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

    if self.path == '/':  # base html
      fp = open("PokeRater.html", "r")
      self.wfile.write(bytes(fp.read(), "utf-8"))
      return
    elif self.path == "/first":  # first pokemon information
      next_id = self.db.get_next_sequential(0)
      pk_info = self.db.get_pokemon_by_id(next_id)
    elif self.path == "/rand":  # random pokemon information
      next_id = self.db.get_next_rand()
      pk_info = self.db.get_pokemon_by_id(next_id)
    elif '?' in self.path:  # sequential
      path, options = self.path.split('?')
      pk_id = self.db.get_id_by_name(options)
      next_id = self.db.get_next_sequential(pk_id)
      pk_info = self.db.get_pokemon_by_id(next_id)
    else:  # gets a specific pokemon
      pk_info = self.db.get_pokemon_by_name(self.path[1:])

    # parse generation info
    generations = self.db.get_generations()
    gens = "["
    for gen in generations:
      avg = self.db.get_average(gen)
      rem = len(self.db.get_unrated_gen_ids(gen))
      gens += "["+str(gen)+','+str(avg)+","+str(rem)+"]"
      if gen != generations[-1]:
        gens += ","
    gens += "]"

    pk_data = '{"name":"'+pk_info[0]+'","urls":'+pk_info[1]+',"gens":'+gens+'}'

    self.wfile.write(bytes(pk_data, "utf-8"))

  def do_POST(self):
    """handles POST requests"""
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    # Gets the post data
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    post_data = json.loads(post_data.decode("utf-8"))

    # sets the rating based on the post data
    self.db.set_rating(post_data["name"], float(post_data["rating"]))

    # send a message to confirm received
    message = "submitted"
    self.wfile.write(bytes(message, "utf8"))


class PKServer:
  """The webserver"""

  def __init__(self, db, host, port):
    """initializes the webserver for the project
    Args:
        db (DB object): database for the project
        host (string): the ip address to link
        port (int): the network port
    """
    self.handler = partial(PKHandler, db)
    self.server = HTTPServer((host, port), self.handler)

  def run(self):
    """runs the webserver"""
    try:
      self.server.serve_forever()
    except KeyboardInterrupt:
      pass

    self.server.server_close()
