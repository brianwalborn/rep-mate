from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
import uuid

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    equipment_id = Column(String, ForeignKey('equipment.id'), nullable=False)
    muscles = Column(JSON, nullable=False)
    archived = Column(Boolean, default=False)

    equipment = relationship("Equipment", backref="exercises")
