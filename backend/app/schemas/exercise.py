from typing import List
from pydantic import BaseModel

class ExerciseBase(BaseModel):
    name: str
    equipment: str
    muscles: List[str]

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseOut(ExerciseBase):
    id: str
    archived: bool

    class Config:
        from_attributes = True
