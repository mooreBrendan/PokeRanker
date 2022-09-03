"""Database for the project """
import sqlite3 as sq3
from random import randint


class DB:
  """Database class to handle database management
  Returns: class instance: an instance of a database
  """

  def __init__(self):
    """initializer for database class"""
    self.conn = sq3.connect("pokeranker.db")
    self.cur = self.conn.cursor()
    self.__init_db()

  def __init_db(self):
    """creates the database for the class"""
    res = self.cur.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ratings'")

    # if the count is 1, then table exists
    if res.fetchone()[0] != 1:
      self.cur.execute(
          "create table ratings(num integer, name text, gen integer, \
            rating integer default 0,sprites text)")

  def already_exists(self, name):
    """checks if a pokemon already exists
    Args: name (text): pokemon name
    Returns: boolean: true if already in database
    """
    self.cur.execute("SELECT rowid FROM ratings WHERE name = ?", (name,))
    data = self.cur.fetchall()
    return len(data) != 0

  def add_entry(self, num, name, gen, sprites):
    """adds a new pokemon to the database

    Args:
        num (number): the pokedex number
        name (text): the pokemon name
        gen (number): the generation number
        sprites (text): comma seperated list of urls
    """
    self.cur.execute(
        f"insert into ratings(num,name,gen,sprites) values ({num},'{name}',{gen},'{sprites}')")
    self.conn.commit()

  def get_ratings(self, gen):
    """gets the ratings for the given generation
    Args: gen (integer): the generation number
    Returns: list: list of ratings
    """
    res = self.cur.execute(
        f"select rating from ratings where gen={gen} and rating != 0")
    return res.fetchall()

  def get_generations(self):
    res = self.cur.execute("Select Distinct gen from ratings")
    return [i[0] for i in res.fetchall()]

  def get_unrated_ids(self):
    """gets the the pokemon ids with no rating
    Returns: list: the ids that are not 0
    """
    res = self.cur.execute("select num from ratings where rating = 0")
    return res.fetchall()

  def get_unrated_gen_ids(self, gen):
    """gets the the pokemon ids with no rating
    Args: gen(number): the generation number
    Returns: list: the ids that are not 0
    """
    res = self.cur.execute(
        f"select num from ratings where rating = 0 and gen={gen}")
    return res.fetchall()

  def get_pokemon_by_id(self, num):
    """returns information on the selected pokemon
    Args: num (number): pokemon id
    Returns: list: the name and sprites for given pokemon
    """
    res = self.cur.execute(
        f"select name, sprites from ratings where num = {num}")
    return res.fetchall()[0]

  def get_pokemon_by_name(self, name):
    """returns information on the selected pokemon
    Args: name (string): pokemon name
    Returns: list: the name and sprites for given pokemon
    """
    res = self.cur.execute(
        f"select name, sprites from ratings where name = '{name}'")
    return res.fetchall()[0]

  def get_id_by_name(self, name):
    res = self.cur.execute(f"select num from ratings where name = '{name}'")
    return res.fetchall()[0][0]

  def set_rating(self, pokemon, rating):
    """sets the rating for the given pokemon

    Args:
        pokemon (text): the name of the pokemon
        rating (number): the rating
    """
    self.cur.execute(
        f"update ratings set rating = {rating} where name='{pokemon}'")
    self.conn.commit()

  def get_average(self, gen):
    arr = self.get_ratings(gen)
    if len(arr) < 1:
      return 0
    sum_val = 0
    for i in arr:
      sum_val += i[0]
    return sum_val/len(arr)

  def get_next_rand(self):
    arr = self.get_unrated_ids()
    return arr[randint(0, len(arr))][0]

  def get_next_sequential(self, curr):
    arr = [i[0] for i in self.get_unrated_ids()]
    out = max(arr)

    # check if need to loop
    if out == curr:
      return min(arr)

    # find next closes value > current
    for i in arr:
      if curr < i < out:
        out = i
    return out
