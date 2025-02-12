from fitness.database.database import get_connection
from fitness.models.workout import Workout
from fitness.models.exercise import Exercise
from psycopg.rows import TupleRow

class WorkoutExercise:
  def __init__(self, row: list[TupleRow] = None, id: str = None) -> None:
    if row:
      self.id: str = row[0]
      self.workout: Workout = Workout(id = row[1])
      self.exercise: Exercise = Exercise(id = row[2])
      self.notes: str = row[3]
      self.date_added: str = row[4]
    elif id:
      self.id: str = id
      self.__get__(id)

  def __get__(self, id: str) -> 'WorkoutExercise':
    database = get_connection()
    exercise = database.execute(f"SELECT * FROM workout_exercises WHERE id = '{id}'").fetchone()

    self.workout: Workout = Workout(id = exercise[1])
    self.exercise: Exercise = Exercise(id = exercise[2])
    self.notes: str = exercise[3]
    self.date_added: str = exercise[4]
