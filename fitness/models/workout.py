from datetime import datetime
from fitness.database.database import get_connection
from psycopg.rows import TupleRow

class Workout:
  def __init__(self, row: list[TupleRow] = None, id: str = None) -> None:
    if row:
      self.id: str = row[0]
      self.name: str = row[1]
      self.notes: str = row[2]
      self.date_added: str = row[3].strftime('%A, %m/%d/%Y %I:%M %p %Z')
    elif id:
      self.id: str = id
      self.__get__(id)

  def __get__(self, id: str) -> 'Workout':
    database = get_connection()
    workouts = database.execute(f"SELECT * FROM workouts WHERE id = '{id}'").fetchone()

    self.name = workouts[1]
    self.notes: str = workouts[2]
    self.date_added = workouts[3].strftime('%A, %m/%d/%Y %I:%M %p %Z')
