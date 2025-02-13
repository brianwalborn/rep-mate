from sqlalchemy import Column, Date, ForeignKeyConstraint, Integer, UUID, text
from tracklift.database.database import database
from tracklift.models.workout_exercise import WorkoutExercise

class Set(database.Model):
  __tablename__ = 'sets'

  id = Column(UUID, default = text('gen_random_uuid()'), primary_key = True)
  workout_exercise_id = Column(UUID, nullable = False)
  repetitions = Column(Integer)
  weight = Column(Integer)
  date_added = Column(Date, default = text("TIMEZONE('utc', NOW())"), nullable = False)

  __table_args__ = (
    ForeignKeyConstraint([workout_exercise_id], [WorkoutExercise.id], ondelete = 'NO ACTION'),
  )

  def __init__(self, id = None, workout_exercise_id = None, repetitions = None, weight = None, date_added = None) -> None:
    self.id: str = id
    self.workout_exercise_id: str = workout_exercise_id
    self.repetitions: int = repetitions
    self.weight: int = weight
    self.date_added: str = date_added

  def __repr__(self) -> str:
    return f"<Set {self.id}>"

  def add(self) -> None:
    database.session.add(self)
    database.session.commit()

  def delete(self) -> None:
    Set.query.filter(Set.workout_exercise_id == self.workout_exercise_id).delete()

    database.session.commit()

  def get(self) -> 'Set':
    response = Set.query.filter(Set.id == self.id).first()

    return response

  def get_all(self) -> list['Set']:
    response = Set.query.filter(Set.workout_exercise_id == self.workout_exercise_id).all()

    return response
