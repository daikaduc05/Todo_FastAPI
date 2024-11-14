from pydantic import BaseModel, EmailStr, Field,model_validator
from typing import Optional
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
from enum import Enum

class PydanticObjectId(ObjectId):
    """ Custom Pydantic type for ObjectId """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError("ObjectId required")
        return str(v)  # Convert ObjectId to str for serialization

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class CustomBase(BaseModel):
    @model_validator(mode="before")
    def convert_objectid_to_str(cls, values):
        for key, value in values.items():
            if isinstance(value, ObjectId):
                values[key] = str(value)  
        return values
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
