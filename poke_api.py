def get_sprites(sprites):
  urls = []
  for key in sprites.keys():
    current = sprites[key]
    if current is not None:
      if isinstance(current, str):
        urls.append(current)
      elif isinstance(current, dict):
        merge = get_sprites(current)
        urls = urls + merge

  return urls


def get_pokemon(generation):
  pass
