import bcrypt
from db.database import retrieve_filter,users,tasks
import jwt
from jwt import DecodeError, ExpiredSignatureError
from bson.objectid import ObjectId
from fastapi import Depends,Header,status,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi import Path
from settings import seceret_key
from schema.users import UserBase
import datetime



def gen_jwt(data: dict) -> str:
    token = jwt.encode(data, seceret_key, algorithm="HS256")
    return token

async def get_user(token : str = Header(...)):
    try:
        user = jwt.decode(token,seceret_key,algorithms="HS256")
        user = jsonable_encoder(user)
        user = await retrieve_filter(users,{"_id" : ObjectId(user["user_id"])})
        user = UserBase.model_validate(user[0])
        return user
    except ExpiredSignatureError:
        return None
    except DecodeError:
        return None

async def authenticated_login(username: str, rqpassword: str) -> str:
    user = await retrieve_filter(users,{"username" : username})
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"invalid username")
    user = UserBase.model_validate(user[0])
    if user:
        password = user.password
        if bcrypt.checkpw(rqpassword.encode('utf-8'), password): 
            expiration_time = datetime.datetime.now() + datetime.timedelta(hours=24)
            payload = { 
                "user_id": str(user.user_id),
                "exp" : expiration_time
            }
            token = gen_jwt(payload)  
            return token
    return None

