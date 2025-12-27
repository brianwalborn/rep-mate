from pydantic import BaseModel

class EquipmentCreate(BaseModel):
    name: str

class EquipmentUpdate(BaseModel):
    name: str

class EquipmentOut(BaseModel):
    id: str
    name: str
    archived: bool

    class Config:
        from_attributes = True
