from fitness.database.database import get_connection
from fitness.models.workout_exercise import WorkoutExercise
from fitness.models.exercise import Exercise
from psycopg.rows import TupleRow

class Set:
  def __init__(self, row: list[TupleRow] = None, id: str = None) -> None:
    if row:
      self.id: str = row[0]
      self.workout: WorkoutExercise = WorkoutExercise(id = row[1])
      self.repetitions: int = row[2]
      self.weight: int = row[3]
      self.date_added: str = row[4]
    elif id:
      self.id: str = id
      self.__get__(id)

  def __get__(self, id: str) -> 'Set':
    database = get_connection()
    this = database.execute(f"SELECT * FROM sets WHERE id = '{id}'").fetchone()

    self.workout: WorkoutExercise = WorkoutExercise(id = this[1])
    self.repetitions: int = this[2]
    self.weight: int = this[3]
    self.date_added: str = this[4]
