from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from uuid import UUID

class UserBaseSchema(BaseModel):
    name: str = Field(..., max_length=255, description="User name")
    email: EmailStr = Field(..., max_length=255, description="The email address of the user")
    
    class Config:
        from_attributes = True
        

class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8)
    
class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="User name")
    email: Optional[EmailStr] = Field(None, description="The email address of the user")
    password: Optional[str] = Field(None, min_length=8, description="The password for the user")
    
    class Config:
        from_attributes = True

class UserResponseSchema(UserBaseSchema):
    id: int
    name: str
    email: EmailStr

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

