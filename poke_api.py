"""Functions for api calls to poke-api """
import json
import requests as re


def parse_sprites(sprites):
  """parses sprites for the given pokemon
  Args: sprites (dictionary): the sprites for the pokemon
  Returns: list: parsed sprites
  """
  urls = []
  for key in sprites.keys():
    current = sprites[key]
    if current is not None:
      if isinstance(current, str):
        urls.append(current)
      elif isinstance(current, dict):
        merge = parse_sprites(current)
        urls = urls + merge

  return urls


def get_generations():
  """Gets the generations from pokemon
  Returns: list: the generations
  """
  generations_api = re.get("https://pokeapi.co/api/v2/generation/")
  if generations_api.status_code == 200:
    return json.loads(generations_api.text)


def get_pokemon(generation):
  """get pokemon from the given generation
  Args: generation (number): the generation
  Returns: list: pokemon from the generation
  """
  generation_api = re.get(generation['url'])
  if generation_api.status_code == 200:
    return json.loads(generation_api.text)['pokemon_species']


def get_sprites(name):
  """gets the sprites
  Args: name (string): the name of the pokemon
  Returns: number,list: pokedex number, sprites
  """
  pokemon_api = re.get("https://pokeapi.co/api/v2/pokemon/" + name)
  if pokemon_api.status_code == 200:
    # parse individual pokemon data
    poke = json.loads(pokemon_api.text)
    sprites = poke['sprites']
    poke_num = poke['id']
    valid = parse_sprites(sprites)
    return poke_num, valid
