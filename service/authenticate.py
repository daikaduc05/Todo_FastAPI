import bcrypt
from db.database import retrieve_filter,users,tasks
import jwt
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from fastapi import Depends,status,HTTPException,Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Path
import json
load_dotenv()

seceret_key = os.getenv("SECERET_KEY")

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def gen_jwt(data: dict) -> str:
    token = jwt.encode(data, seceret_key, algorithm="HS256")
    return token

async def get_user(token : str = Header(...)) -> dict:
    try:
        user = jwt.decode(token,seceret_key,algorithms="HS256")
        user = jsonable_encoder(user)
        if await retrieve_filter(users,{"_id" : ObjectId(user["user_id"])}):
            return user
        else:
            raise ValueError("")
    except jwt.InvalidTokenError:
        return JSONResponse(
            content={
                "error" : "invalid Token"
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

async def authenticated_login(username: str, rqpassword: str) -> str:
    user = await retrieve_filter(users,{"username" : username})
    if user:
        password = user["password"]
        user.pop("password") 
        if bcrypt.checkpw(rqpassword.encode('utf-8'), password): 
            token = gen_jwt({"username": user["username"], "user_id": user["_id"],"role" : user["role"]} )  
            return token
    return None

class RoleBaseAccessControl:
    def __init__(self,allowed_role,action):
        self.allowed_role = allowed_role
        self.action = action
    async def __call__(self,user : dict = Depends(get_user),task_id : str = Path()):
        task = await retrieve_filter(tasks,{"_id" : ObjectId(task_id)})
      
        if not isinstance(user,dict):
            return user
        data = {
            "task_id" : task_id,
            "action" : self.action,
            "allowed_role" : self.allowed_role            
        }
        if user["role"] in self.allowed_role or user["user_id"] == task["assigned_to"]:
            return data
        else:
        
            if self.action == "retrieve":
                if task["every_one"] == True:
                    return data
                
                for key,value in task["share_with"].items():
                    #print(value)
                    if value == user["user_id"]:
                         return data
            # #     if user["user_id"] in task["share_with"].values():
            # #         return data
            return JSONResponse(
                content={
                    "error" : "not permission"
                },
                status_code=status.HTTP_403_FORBIDDEN
            )

