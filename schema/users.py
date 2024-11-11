from pydantic import BaseModel, EmailStr, Field,field_validator
from typing import Optional
from fastapi.responses import JSONResponse
import re
import enum

class RegisterRequest(BaseModel):
    username : str = Field(...,min_length=3,max_length=30)
    password : str = Field(...,min_length=8,max_length=100)
    email : EmailStr = Field(...)
    @field_validator("password")
    def valid(cls,password):
        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if re.match(pattern,password):
            return password
        raise ValueError("The password must be created by at least 1 number character,1 special character,1 uppercase character,1 lowercase character, 8 character")
    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example" : {
                "username" : "daikaduk05",
                "password" : "121Ad@fa",
                "email" : "danghoaiduc90@gmail.com",
            }
        }

class LoginRequest(BaseModel):
    username : str = Field(...,min_length=3,max_length=30)
    password : str = Field(...,min_length=8,max_length=100)
    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example" : {
                "username" : "daikaduk05",
                "password" : "121Ad@fa",
            }
        }


