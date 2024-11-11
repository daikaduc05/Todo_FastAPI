import bcrypt
from db.database import retrieve_filter,users,tasks
import jwt
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.errors import InvalidId
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

class RoleBaseAccessControlWithTask:
    def __init__(self,allowed_role,action):
        self.allowed_role = allowed_role
        self.action = action
    async def __call__(self,user = Depends(get_user),task_id : str = Path()):
        try:
            task = await retrieve_filter(tasks,{"_id" : ObjectId(task_id)})
        except InvalidId:
            return JSONResponse(content={
                "error" : "id is not true form objectid"
            },status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
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
                if task["every_one"] == "True":
                    return data
                for value in task["share_with"]:
                    if value == user["user_id"]:
                         return data
            
        return JSONResponse(
                content={
                    "error" : "not permission"
                },
                status_code=status.HTTP_403_FORBIDDEN
            )

class RoleBaseAccessControlWithUser:
    def __init__(self,allowed_role,action):
        self.allowed_role = allowed_role
        self.action = action
    async def __call__(self,this_user = Depends(get_user),another_user : str = Path()):
        try:
            another_user = await retrieve_filter(users,{"_id" : ObjectId(another_user)})
        except InvalidId:
            return JSONResponse(content={
                "error" : "id is not true form objectid"
            },status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not isinstance(this_user,dict):
            return this_user
        data = {
            "_id" : another_user["_id"],
            "action" : self.action 
        }
        print(this_user["role"])
        if this_user["role"] in self.allowed_role:
            return data
        return JSONResponse(
                content={
                    "error" : "not permission"
                },
                status_code=status.HTTP_403_FORBIDDEN
            )
