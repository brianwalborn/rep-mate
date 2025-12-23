from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import uuid

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    date = Column(DateTime, nullable=False)  # Changed from Date to DateTime
    duration = Column(Integer, default=0)  # Duration in minutes

    exercises = relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete"
    )
