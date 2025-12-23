from sqlalchemy import Column, String, Boolean
from app.database import Base
import uuid

class Muscle(Base):
    __tablename__ = "muscles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    archived = Column(Boolean, default=False)
