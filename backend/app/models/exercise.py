from app.database import Base
from sqlalchemy import Boolean, Column, JSON, String
import uuid

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    equipment = Column(String, nullable=False)
    muscles = Column(JSON, nullable=False)
    archived = Column(Boolean, default=False)
