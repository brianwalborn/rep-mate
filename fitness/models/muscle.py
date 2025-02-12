from fitness.database.database import get_connection
from psycopg.rows import TupleRow

class Muscle:
  def __init__(self, row: list[TupleRow] = None, id: str = None) -> None:
    if row:
      self.id: str = row[0]
      self.name: str = row[1]
      self.date_added: str = row[2]
    elif id:
      self.id: str = id
      self.__get__(id)

  def __get__(self, id: str) -> 'Muscle':
    database = get_connection()
    response = database.execute(f"SELECT * FROM muscles WHERE id = '{id}'").fetchone()

    self.name = response[1]
    self.date_added = response[2]
