from pydantic import BaseModel, EmailStr, Field,field_validator,model_validator
from typing import Optional
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
from enum import Enum
from .basecustom import CustomBase

class ActionName(str,Enum):
    create = "create"
    update = "update"
    retrieve = "retrieve"
    delete = "delete"

class ActionBase(CustomBase):
    action_id : str = Field(None,alias="_id")
    action_name : ActionName = Field(None)
    
