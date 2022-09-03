"""main function that calls the others"""
import poke_api as pk
import db
from pk_server import pkServer

if __name__ == "__main__":
  print("starting initializing")

  print("creating db")
  pokedb = db.DB()

  # print("filling db")
  # generations = pk.get_generations()
  # for gen_num, generation in enumerate(generations['results']):
  #   pokemon = pk.get_pokemon(generation)
  #   for poke in pokemon:
  #     name = poke['name']
  #     print(f"{name=}")
  #     if not pokedb.already_exists(name):
  #       print("adding")
  #       poke_num, sprites = pk.get_sprites(name, poke['url'])
  #       pokedb.add_entry(poke_num, name, gen_num+1,
  #                        '["' + '","'.join(sprites)+'"]')

  print("done initializing")
  server = pkServer(pokedb, "localhost", 8080)
  server.run()

  # pokedb.set_rating("ditto", 4.5)
  # pokedb.set_rating("vaporeon", 5.0)
  # # pokedb.set_rating("charizard", 3.5)
  # # pokedb.set_rating("chimchar", 4.0)
#
  # # avg1 = pokedb.get_average(1)
  # # rem1 = len(pokedb.get_unrated_gen_ids(1))
#
  # # avg4 = pokedb.get_average(4)
  # # rem4 = len(pokedb.get_unrated_gen_ids(4))
  # # print(f"4: {avg1=}:{rem1=}, {avg4=}:{rem4=}")
#
  # # temp = pokedb.get_pokemon_by_id(151)
  # # print("151: ", temp)
#
  # # temp = pokedb.get_pokemon_by_name("articuno")
  # # print("Articuno: ", temp)
#
  # # temp = pokedb.get_next_rand()
  # # print(f"rand: {temp}")
#
  # # temp = pokedb.get_next_sequential(71)
  # # print(f"rand: {temp}")
#
