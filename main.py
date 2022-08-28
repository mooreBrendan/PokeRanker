"""main function that calls the others"""
import poke_api as pk
import db

if __name__ == "__main__":
  print("starting initializing")

  print("creating db")
  pokedb = db.DB()

  print("filling db")
  generations = pk.get_generations()
  for gen_num, generation in enumerate(generations):
    pokemon = pk.get_pokemon(generation)
    for poke in pokemon:
      name = poke['name']
      if not pokedb.already_exists(name):
        poke_num, sprites = pk.get_sprites(name)
        pokedb.add_entry(poke_num, name, gen_num, sprites.join(','))

  print("done initializing")
