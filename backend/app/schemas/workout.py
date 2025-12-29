from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class SetCreate(BaseModel):
    weight: float
    reps: int
    completed: Optional[bool] = False

class WorkoutExerciseCreate(BaseModel):
    exercise_id: str
    name: str  # Accept 'name' from frontend
    notes: Optional[str] = ''
    sets: List[SetCreate]

class WorkoutCreate(BaseModel):
    date: datetime  # Accept ISO datetime string from frontend
    duration: Optional[int] = 0  # Duration in minutes
    exercises: List[WorkoutExerciseCreate]

class SetOut(BaseModel):
    id: str
    weight: float
    reps: int
    completed: bool

    class Config:
        from_attributes = True

class WorkoutExerciseOut(BaseModel):
    id: str
    exercise_id: str
    exercise_name: str
    muscles: Optional[List[str]] = []
    notes: Optional[str] = ''
    sets: List[SetOut]

    class Config:
        from_attributes = True

class WorkoutOut(BaseModel):
    id: str
    date: datetime
    duration: int
    exercises: List[WorkoutExerciseOut]

    class Config:
        from_attributes = True

