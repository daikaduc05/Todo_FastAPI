from pydantic import BaseModel, EmailStr, Field,field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from bson import ObjectId
from .basecustom import CustomBase
class Status(str,Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskBase(CustomBase):
    task_id : str = Field(None,alias="_id")
    description : str = Field(...)
    status : Status = Field(...)
    share_with : list = Field(None)
    due_to : datetime = Field(...)
    user_id : str = Field(...)
    public : bool = Field(...)
    class Config:
        alias_generator = lambda field: field if field != "task_id" else "_id"

class TaskCreateRequest(BaseModel):
    description : str = Field(...)
    status : Status = Field(...)
    share_with : list = Field(None)
    due_to : datetime = Field(...)
    public : bool = Field(...)

class TaskUpdateRequest(BaseModel):
    description : str = Field(None)
    status : Status = Field(None)
    share_with : list = Field(None)
    due_to : datetime = Field(None)
    public : bool = Field(None)
    
