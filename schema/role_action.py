from pydantic import BaseModel, EmailStr, Field,field_validator
from typing import Optional
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
from enum import Enum
from .resources import ResourceBase
from .basecustom import CustomBase
class RoleAction(CustomBase):
    role_action_id : str = Field(None,alias="_id")
    role_id : str = Field(...)
    action_id : str = Field(...)
    resource_id : str = Field(...)
    just_for_owner : bool = Field(...)


