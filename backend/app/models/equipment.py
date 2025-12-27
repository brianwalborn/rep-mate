from app.database import Base
from sqlalchemy import Boolean, Column, String
import uuid

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    archived = Column(Boolean, default=False)
