from pydantic import BaseModel, EmailStr, Field,model_validator
from typing import Optional
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
from enum import Enum
from .resources import ResourceBase
from .basecustom import CustomBase
class RoleName(str,Enum):
    admin = "admin"
    user = "user"

class RoleBase(CustomBase):
    role_id : str = Field(...,alias="_id")
    role_name : RoleName = Field(...)
    resource_id : str = Field(...)

class RoleRequest(BaseModel):
    role_name : RoleName

