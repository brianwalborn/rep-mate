from sqlalchemy import Column, DateTime, ForeignKeyConstraint, String, UUID, text
from repmate.database.database import database
from repmate.models.exercise import Exercise
from repmate.models.workout import Workout

class WorkoutExercise(database.Model):
  __tablename__ = 'workout_exercises'

  id = Column(UUID, server_default = text('gen_random_uuid()'), primary_key = True)
  workout_id = Column(UUID, nullable = False)
  exercise_id = Column(UUID, nullable = False)
  notes = Column(String)
  date_added = Column(DateTime, server_default = text("TIMEZONE('utc', NOW())"), nullable = False)

  __table_args__ = (
    ForeignKeyConstraint([workout_id], [Workout.id], ondelete = 'NO ACTION'),
    ForeignKeyConstraint([exercise_id], [Exercise.id], ondelete = 'NO ACTION')
  )

  def __init__(self, id = None, workout_id = None, exercise_id = None, notes = None, date_added = None) -> None:
    self.id: str = id
    self.workout_id: str = workout_id
    self.exercise_id: str = exercise_id
    self.notes: str = notes
    self.date_added: str = date_added

  def __repr__(self) -> str:
    return f"<WorkoutExercise {self.id}>"

  def add(self) -> None:
    database.session.add(self)
    database.session.commit()

  def delete(self) -> None:
    WorkoutExercise.query.filter(WorkoutExercise.workout_id == self.workout_id).delete()

    database.session.commit()

  def get(self) -> 'WorkoutExercise':
    response = WorkoutExercise.query.filter(WorkoutExercise.workout_id == self.workout_id, WorkoutExercise.exercise_id == self.exercise_id).first()

    return response

  def get_all(self) -> list['WorkoutExercise']:
    response = WorkoutExercise.query.filter(WorkoutExercise.workout_id == self.workout_id).all()

    return response
