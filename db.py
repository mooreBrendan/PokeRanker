"""Database for the project """
import sqlite3 as sq3


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
    res = self.cur.execute(f"select ratings from ratings where gen={gen}")
    return res.fetchall()

  def get_unrated_ids(self):
    """gets the the pokemon ids with no rating
    Returns: list: the ids that are not 0
    """
    res = self.cur.execute("select num from ratings where not rating=0")
    return res.fetchall()

  def get_pokemon(self, num):
    """returns information on the selected pokemon
    Args: num (number): pokemon id
    Returns: list: the name and sprites for given pokemon
    """
    res = self.cur.execute(
        f"select name, sprites from ratings where id = {num}")
    return res.fetchall()

  def set_rating(self, pokemon, rating):
    """sets the rating for the given pokemon

    Args:
        pokemon (text): the name of the pokemon
        rating (number): the rating
    """
    self.cur.execute(
        f"update ratings set rating = {rating} where name='{pokemon}'")
    self.conn.commit()
