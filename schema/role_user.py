from pydantic import BaseModel, EmailStr, Field,field_validator
from typing import Optional
from pydantic import model_validator
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
from enum import Enum
from .basecustom import CustomBase

class RoleUser(CustomBase):
    role_user_id : str = Field(None,alias="_id")
    role_id : str = Field(...)
    user_id : str = Field(...)

