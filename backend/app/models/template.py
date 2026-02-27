from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Template(Base):
    __tablename__ = "templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    exercises = relationship(
        "TemplateExercise",
        back_populates="template",
        cascade="all, delete-orphan",
        order_by="TemplateExercise.order"
    )


class TemplateExercise(Base):
    __tablename__ = "template_exercises"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_id = Column(String, ForeignKey("templates.id"), nullable=False)
    exercise_id = Column(String, ForeignKey("exercises.id"), nullable=False)
    order = Column(Integer, nullable=False)  # Order of exercise in template
    notes = Column(String, nullable=True)

    template = relationship("Template", back_populates="exercises")
    exercise = relationship("Exercise")
    sets = relationship(
        "TemplateSet",
        back_populates="template_exercise",
        cascade="all, delete-orphan",
        order_by="TemplateSet.set_number"
    )


class TemplateSet(Base):
    __tablename__ = "template_sets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_exercise_id = Column(String, ForeignKey("template_exercises.id"), nullable=False)
    set_number = Column(Integer, nullable=False)
    weight = Column(Float, nullable=True)  # Optional - can be null
    reps = Column(Integer, nullable=True)  # Optional - can be null
    unit = Column(String, default='lbs', nullable=False)

    template_exercise = relationship("TemplateExercise", back_populates="sets")
