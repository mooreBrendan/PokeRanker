import requests as re
import json
import poke_api as pk
import db

if __name__ == "__main__":
  print("starting")
  generations_api = re.get("https://pokeapi.co/api/v2/generation/")

  # get all of the generations
  if generations_api.status_code == 200:
    generations = json.loads(generations_api.text)
    print(generations['results'])

    # parse through generations
    for generation in generations:
      generation_api = re.get(generation['url'])
      if generation_api.status_code == 200:
        species = json.loads(generation_api.text)['pokemon_species']

        # parse through pokemon in each generation
        for pokemon in species:
          pokemon_api = re.get(
              "https://pokeapi.co/api/v2/pokemon/" + pokemon['name'])
          if pokemon_api.status_code == 200:
            # parse individual pokemon data
            poke = json.loads(pokemon_api.text)
            name = poke['name']
            sprites = poke['sprites']
            valid = pk.get_sprites(sprites)

            # DEBUG: remove print statement below
            print(valid)
  print("done")
