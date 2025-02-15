from sqlalchemy import Column, DateTime, ForeignKeyConstraint, String, UUID, text
from repmate.database.database import database
from repmate.models.equipment import Equipment
from repmate.models.muscle import Muscle

class Exercise(database.Model):
  __tablename__ = 'exercises'

  id = Column(UUID, server_default = text('gen_random_uuid()'), primary_key = True)
  name = Column(String, unique = True, nullable = False)
  description = Column(String)
  muscle_id = Column(UUID)
  equipment_id = Column(UUID, nullable = False)
  date_added = Column(DateTime, server_default = text("TIMEZONE('utc', NOW())"), nullable = False)

  __table_args__ = (
    ForeignKeyConstraint([muscle_id], [Muscle.id], ondelete = 'NO ACTION'),
    ForeignKeyConstraint([equipment_id], [Equipment.id], ondelete = 'NO ACTION')
  )

  def __init__(self, id = None, name = None, description = None, muscle_id = None, equipment_id = None, date_added = None) -> None:
    self.id: str = id
    self.name: str = name
    self.description: str = description
    self.muscle_id: str = muscle_id
    self.equipment_id: str = equipment_id
    self.date_added: str = date_added

  def __repr__(self) -> str:
    return f"<Exercise {self.name}>"

  def add(self) -> None:
    database.session.add(self)
    database.session.commit()

  def delete(self) -> None:
    Exercise.query.filter(Exercise.id == self.id).delete()

    database.session.commit()

  def get(self) -> 'Exercise':
    response = Exercise.query.filter(Exercise.id == self.id).first()

    return response

  def get_all(self) -> list['Exercise']:
    response = Exercise.query.all()

    return response

  def update(self):
    Exercise.query.filter(Exercise.id == self.id).update({Exercise.name: self.name})
    Exercise.query.filter(Exercise.id == self.id).update({Exercise.description: self.description})
    Exercise.query.filter(Exercise.id == self.id).update({Exercise.muscle_id: self.muscle_id})
    Exercise.query.filter(Exercise.id == self.id).update({Exercise.equipment_id: self.equipment_id})

    database.session.commit()
