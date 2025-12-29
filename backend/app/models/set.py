from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workout_id = Column(String, ForeignKey("workouts.id"))
    exercise_id = Column(String)
    exercise_name = Column(String)
    muscles = Column(JSON, nullable=True)  # Add muscles field for denormalized data
    notes = Column(String, nullable=True)  # Add notes field for exercise notes

    workout = relationship("Workout", back_populates="exercises")
    sets = relationship(
        "Set",
        back_populates="exercise",
        cascade="all, delete"
    )

class Set(Base):
    __tablename__ = "sets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workout_exercise_id = Column(String, ForeignKey("workout_exercises.id"))
    weight = Column(Float)  # Changed from Integer to Float
    reps = Column(Integer)
    completed = Column(Boolean, default=False)  # Added completed field

    exercise = relationship("WorkoutExercise", back_populates="sets")
