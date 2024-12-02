from pydantic import BaseModel, EmailStr, Field,field_validator
from typing import Optional
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
from enum import Enum
from .basecustom import CustomBase
class ResourceBase(CustomBase):
    resource_id : str = Field(None,alias="_id")
    resource_name : str = Field(None)
