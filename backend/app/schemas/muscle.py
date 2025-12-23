from pydantic import BaseModel

class MuscleBase(BaseModel):
    name: str

class MuscleCreate(MuscleBase):
    pass

class MuscleUpdate(MuscleBase):
    pass

class MuscleOut(MuscleBase):
    id: str
    archived: bool

    class Config:
        from_attributes = True
