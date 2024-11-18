from pydantic import  Field,field_validator,BaseModel, EmailStr
from bson import ObjectId
import re
from .roles import RoleName
from.basecustom import CustomBase
from service.validate import hash_password

class UserBase(CustomBase):
    user_id : str = Field(None,alias="_id")
    email : EmailStr = Field(None)
    username : str = Field(...,min_length=3,max_length=30)
    password : bytes = Field(...)
    create_id : str = Field(None)
    class Config:
        json_schema_extra = {
            "example" : {
                "username" : "daikaduk05",
                "password" : "121Ad@fa",
            }
        }

class UserResponse(CustomBase):
    user_id : str = Field(None,alias="_id")
    username : str = Field(...,min_length=3,max_length=30)
    email : EmailStr = Field(None)
    create_id : str = Field(None)
    class Config:
        alias_generator = lambda field: field if field != "user_id" else "_id"



class LoginRequest(BaseModel):
    username : str = Field(...,min_length=3,max_length=30)
    password : str = Field(...,min_length=8,max_length=100)
    class Config:
        json_schema_extra = {
            "example" : {
                "username" : "daikaduk05",
                "password" : "121Ad@fa",
            }
        }

class ValidateRequest(BaseModel):
    email : EmailStr = Field(...)
    otp : str = Field(...)

class UserRequest(BaseModel):
    username : str = Field(...,min_length=3,max_length=30)
    email : str = Field(...,min_length=3,max_length=30)
    password : bytes = Field(...,min_length=8,max_length=100)
    @field_validator("password",mode="before")
    def valid(cls,password):
        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
        if re.match(pattern,password):
            return hash_password(password)
        raise ValueError("The password must be created by at least 1 number character,1 special character,1 uppercase character,1 lowercase character, 8 character")
    class Config:
        json_schema_extra = {
            "example" : {
                "email" : "tranthigianhan1807@gmail.com",
                "username" : "daikaduk05",
                "password" : "121Ad@fa",
            }
        }

class CreateUserRequest(UserRequest):
    role_name : RoleName 
    class Config:
        json_schema_extra = {
            "example" : {
                "username" : "daikaduk05",
                "password" : "121Ad@fa",
                "role_name" : "admin"
            }
        }

class UpdateUserRequest(BaseModel):
    username : str = Field(None,min_length=3,max_length=30)
    password : bytes = Field(None,min_length=8,max_length=100)
    @field_validator("password",mode="before")
    def valid(cls,password):
        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
        if re.match(pattern,password):
            return hash_password(password)
        raise ValueError("The password must be created by at least 1 number character,1 special character,1 uppercase character,1 lowercase character, 8 character")