"""main function that calls the others"""
import poke_api as pk
import db
from pk_server import PKServer

if __name__ == "__main__":
  print("starting initializing")
  HOST_NAME = "localhost"
  SERVER_PORT = 8080

  print("creating db")
  pokedb = db.DB()

  print("filling db")
  generations = pk.get_generations()
  for gen_num, generation in enumerate(generations['results']):
    pokemon = pk.get_pokemon(generation)
    for poke in pokemon:
      name = poke['name']
      print(f"{name=}")
      if not pokedb.already_exists(name):
        print("adding")
        poke_num, sprites = pk.get_sprites(name, poke['url'])
        pokedb.add_entry(poke_num, name, gen_num+1,
                         '["' + '","'.join(sprites)+'"]')

  print("done initializing")
  server = PKServer(pokedb, HOST_NAME, SERVER_PORT)
  server.run()
