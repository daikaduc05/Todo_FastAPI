from pydantic import BaseModel, EmailStr, Field,field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
class Status(str,Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskCreateRequest(BaseModel):
    description : str = Field(...)
    due_to : datetime = Field(...)
    status : Status = Field(...)
    share_with : Optional[list] = None
    every_one : bool = Field(...)
 
    class Config:
        extra = 'forbid'
    

class TaskUpdateRequest(BaseModel):
    description : Optional[str] = None
    due_to : Optional[datetime] = None
    status : Optional[Status] = None
    share_with : Optional[list] = None
    every_one : Optional[bool] = None
    class Config:
        extra = 'forbid'

