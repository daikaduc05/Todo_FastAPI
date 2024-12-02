from pydantic import BaseModel, EmailStr, Field,model_validator
from typing import Optional
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
from enum import Enum

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
