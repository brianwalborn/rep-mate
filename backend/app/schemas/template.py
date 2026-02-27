from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class TemplateSetCreate(BaseModel):
    set_number: int
    weight: Optional[float] = None
    reps: Optional[int] = None
    unit: str = 'lbs'


class TemplateSetOut(BaseModel):
    id: str
    set_number: int
    weight: Optional[float] = None
    reps: Optional[int] = None
    unit: str

    class Config:
        from_attributes = True


class TemplateExerciseCreate(BaseModel):
    exercise_id: str
    order: int
    notes: Optional[str] = None
    sets: List[TemplateSetCreate]


class TemplateExerciseOut(BaseModel):
    id: str
    exercise_id: str
    order: int
    notes: Optional[str] = None
    sets: List[TemplateSetOut]
    # Include exercise details for frontend convenience
    exercise_name: Optional[str] = None
    equipment: Optional[str] = None
    muscles: Optional[List[str]] = None

    class Config:
        from_attributes = True


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    exercises: List[TemplateExerciseCreate]


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    exercises: Optional[List[TemplateExerciseCreate]] = None


class TemplateOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    exercises: List[TemplateExerciseOut]

    class Config:
        from_attributes = True


class TemplateSummary(BaseModel):
    """Lightweight template info for listing"""
    id: str
    name: str
    description: Optional[str] = None
    exercise_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
