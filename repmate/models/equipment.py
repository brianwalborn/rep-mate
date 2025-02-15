from sqlalchemy import Column, DateTime, String, UUID, text
from repmate.database.database import database

class Equipment(database.Model):
  __tablename__ = 'equipment'

  id = Column(UUID, server_default = text('gen_random_uuid()'),  primary_key = True)
  name = Column(String, unique = True, nullable = False)
  date_added = Column(DateTime, server_default = text("TIMEZONE('utc', NOW())"), nullable = False)

  def __init__(self, id = None, name = None, date_added = None) -> None:
    self.id: str = id
    self.name: str = name
    self.date_added: str = date_added

  def __repr__(self) -> str:
    return f"<Equipment {self.name}>"

  def add(self) -> None:
    database.session.add(self)
    database.session.commit()

  def delete(self) -> None:
    Equipment.query.filter(Equipment.id == self.id).delete()

    database.session.commit()

  def get(self) -> 'Equipment':
    response = Equipment.query.filter(Equipment.id == self.id).first()

    if not response:
      response = Equipment.query.filter(Equipment.name == self.name).first()

    return response

  def get_all(self) -> list['Equipment']:
    response = Equipment.query.all()

    return response

  def update(self):
    Equipment.query.filter(Equipment.id == self.id).update({Equipment.name: self.name})

    database.session.commit()
