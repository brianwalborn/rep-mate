from typing import List
from pydantic import BaseModel

class ExerciseBase(BaseModel):
    name: str
    equipment_id: str
    muscles: List[str]

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseOut(BaseModel):
    id: str
    name: str
    equipment: str  # Will be populated from relationship
    muscles: List[str]
    archived: bool

    class Config:
        from_attributes = True
