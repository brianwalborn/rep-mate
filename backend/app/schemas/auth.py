from typing import Optional
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfile(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    weight_unit: str = 'lbs'

    class Config:
        from_attributes = True

class UpdateProfile(BaseModel):
    name: Optional[str] = None
    weight_unit: Optional[str] = None
