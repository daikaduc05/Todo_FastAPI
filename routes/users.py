from fastapi import APIRouter,Body,HTTPException,status,Depends
from fastapi.encoders import jsonable_encoder
from service.authenticate import authenticated_login
from fastapi.responses import JSONResponse
from schema.users import(
    RegisterRequest,
    LoginRequest
)
from service.authenticate import(
    RoleBaseAccessControlWithUser
)
from db.database import(
    users,
    create,
    retrieve_filter,
    update
)
from service.authenticate import(
    hash_password
)

router = APIRouter()


@router.post("/register/")
async def register(user_data : RegisterRequest = Body(...)):
    user_data = jsonable_encoder(user_data) #encode registerrequest from pydantic to json(dict)
    email = user_data["email"]
    username = user_data["username"]
    user_data["role"] = "user"
    if await retrieve_filter(users,{"email":email}):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Exist email")
    else:
        if await retrieve_filter(users,{"username":username}):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"Exist username")
        else:
            user_data['password'] = hash_password(user_data['password'])
            user = await create(users,user_data)
            return user

@router.post("/login/")
async def login(login_data : LoginRequest = Body(...)):
    login_data = jsonable_encoder(login_data)
    username = login_data["username"]
    password = login_data["password"]
    token = await authenticated_login(username,password)
    if token :
        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "token": token
                }
            )
    else :
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid username/password")
    
@router.patch("/up_level/{another_user}")
async def up_level(permission : dict = Depends(RoleBaseAccessControlWithUser({"admin"},"up_level"))):
    if not isinstance(permission,dict):
        return permission
    print(permission)
    data = {
        "role" : "admin"
    }
    user = await update(users,permission["_id"],data)
    return user
    

