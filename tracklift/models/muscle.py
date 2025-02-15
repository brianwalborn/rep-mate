from sqlalchemy import Column, DateTime, String, UUID, text
from tracklift.database.database import database

class Muscle(database.Model):
  __tablename__ = 'muscles'

  id = Column(UUID, server_default = text('gen_random_uuid()'), primary_key = True)
  name = Column(String, unique = True, nullable = False)
  date_added = Column(DateTime, server_default = text("TIMEZONE('utc', NOW())"), nullable = False)

  def __init__(self, id = None, name = None, date_added = None) -> None:
    self.id: str = id
    self.name: str = name
    self.date_added: str = date_added

  def __repr__(self) -> str:
    return f"<Muscle {self.name}>"

  def add(self) -> None:
    database.session.add(self)
    database.session.commit()

  def delete(self) -> None:
    Muscle.query.filter(Muscle.id == self.id).delete()

    database.session.commit()

  def get(self) -> 'Muscle':
    response = Muscle.query.filter(Muscle.id == self.id).first()

    if not response:
      response = Muscle.query.filter(Muscle.name == self.name).first()

    return response

  def get_all(self) -> list['Muscle']:
    response = Muscle.query.all()

    return response

  def update(self):
    Muscle.query.filter(Muscle.id == self.id).update({Muscle.name: self.name})

    database.session.commit()
