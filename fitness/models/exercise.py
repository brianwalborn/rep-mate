from fitness.database.database import get_connection
from fitness.models.equipment import Equipment
from fitness.models.muscle import Muscle
from psycopg.rows import TupleRow

class Exercise:
  def __init__(self, row: list[TupleRow] = None, id = None) -> None:
    if row:
      self.id: str = row[0]
      self.name: str = row[1]
      self.description: str = row[2]
      self.muscle: Muscle = Muscle(id = row[3])
      self.equipment: Equipment = Equipment(id = row[4])
      self.date_added: str = row[5]
    elif id:
      self.id: str = id
      self.__get__(id)

  def __get__(self, id: str) -> 'Exercise':
    database = get_connection()
    response = database.execute(f"SELECT * FROM exercises WHERE id = '{id}'").fetchone()

    self.name = response[1]
    self.description: str = response[2]
    self.muscle: Muscle = Muscle(id = response[3])
    self.equipment: Equipment = Equipment(id = response[4])
    self.date_added = response[5]
