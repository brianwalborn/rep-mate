from sqlalchemy import Column, DateTime, String, UUID, text
from repmate.database.database import database

class Workout(database.Model):
  __tablename__ = 'workouts'

  id = Column(UUID, server_default = text('gen_random_uuid()'), primary_key = True)
  name = Column(String, unique = True)
  notes = Column(String)
  date_added = Column(DateTime, server_default = text("TIMEZONE('utc', NOW())"), nullable = False)

  def __init__(self, id = None, name = None, notes = None, date_added = None) -> None:
    self.id: str = id
    self.name: str = name
    self.notes: str = notes
    self.date_added: str = date_added

  def __repr__(self) -> str:
    return f"<Workout {self.name}>"

  def add(self) -> None:
    database.session.add(self)
    database.session.commit()

  def delete(self) -> None:
    Workout.query.filter(Workout.id == self.id).delete()

    database.session.commit()

  def get(self) -> 'Workout':
    response = Workout.query.filter(Workout.id == self.id).first()

    return response

  def get_all(self) -> list['Workout']:
    response = Workout.query.all()

    return response

#self.date_added = workouts[3].strftime('%A, %m/%d/%Y %I:%M %p %Z')
