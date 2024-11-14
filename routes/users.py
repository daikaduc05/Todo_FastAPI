from fastapi import APIRouter,Body,Path,HTTPException,status,Depends
from fastapi.encoders import jsonable_encoder
from service.authenticate import authenticated_login
from fastapi.responses import JSONResponse
from schema.users import(
    UserBase,
    UserResponse,
    UserRequest,
    CreateUserRequest,
    UpdateUserRequest,
    LoginRequest
)
from bson import ObjectId
from bson.errors import InvalidId
from db.database import(
    users,
    create,
    retrieve_filter,
    resources,
    roles,
    roles_users,
    actions,
    update,
    delete
)

from service.authenticate import get_user
from service.authorize import role_base
from schema.roles import RoleBase,RoleRequest
from schema.actions import ActionBase
from schema.resources import ResourceBase
from schema.response import Response
from schema.role_user import RoleUser
router = APIRouter()
    
from service.validate import validict

@router.post("/register/")
async def register(user_data : UserRequest = Body(...)) -> UserResponse:
    username = user_data.username
    role = await retrieve_filter(roles,{"role_name" : "user"})
    role = RoleBase.model_validate(role[0])
    if await retrieve_filter(users,{"username":username}):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Exist username")
    else:
        user_data = user_data.model_dump()
        user = await create(users,user_data)
        user = UserResponse.model_validate(user)
        role_user_data = {
            "role_id" : ObjectId(role.role_id),
            "user_id" : ObjectId(user.user_id)
        }
        await create(roles_users,role_user_data)
        return user

        

@router.post("/login/")
async def login(login_data : LoginRequest = Body(...)) -> str:
    username = login_data.username
    password = login_data.password
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

@router.post("/create_user/")
async def create_user(user_data : CreateUserRequest = Body(...),this_user : UserBase = Depends(get_user)):
    try:
        if not this_user:
            response = Response(
                detail="unauthorize user"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_401_UNAUTHORIZED,
            )
        action = await retrieve_filter(actions,{"action_name" : "create"})
        action = ActionBase.model_validate(action[0])
        resource = await retrieve_filter(resources,{"resource_name" : "user"})
        resource = ResourceBase.model_validate(resource[0])
        check_role = await role_base(this_user,action,resource,False)
        if check_role == False:
            response = Response(
                detail="user does not have permission"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_403_FORBIDDEN,
            )
        if await retrieve_filter(users,{"username" : user_data.username}):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"Exist username")
        role = await retrieve_filter(roles,{"role_name" : user_data.role_name})
        role = RoleBase.model_validate(role[0])
        user_data = user_data.model_dump()
        user_data["create_id"] = this_user.user_id
        user_data = UserBase.model_validate(user_data)
        user = await create(users,validict(user_data.model_dump()))
        user = UserResponse.model_validate(user)
        role_user_data = {"user_id" : ObjectId(user.user_id),"role_id" : ObjectId(role.role_id)}
        await create(roles_users,role_user_data)
        return user
    except InvalidId:
        raise HTTPException(422,"wrong object id form")

@router.patch("/update_user/{user_id}")
async def update_user(user_id = Path(...) ,user_data : UpdateUserRequest = Body(...),this_user : UserBase = Depends(get_user)):
    try:
        if not this_user:
            response = Response(
                detail="unauthorize user"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_401_UNAUTHORIZED,
            )
        user_is_exist = await retrieve_filter(users,{"_id" : ObjectId(user_id)})
        if user_is_exist is None:
            raise HTTPException(404,"user does not exist")
        if not this_user:
            response = Response(
                detail="unauthorize user"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_401_UNAUTHORIZED,
            )
        action = await retrieve_filter(actions,{"action_name" : "update"})
        action = ActionBase.model_validate(action[0])
        resource = await retrieve_filter(resources,{"resource_name" : "user"})
        resource = ResourceBase.model_validate(resource[0])
        check_role = await role_base(this_user,action,resource,user_id == this_user.user_id)
        if check_role == False:
            response = Response(
                detail="user does not have permission"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_403_FORBIDDEN,
            )
        user_data = validict(user_data.model_dump())
        await update(users,ObjectId(user_id),user_data)
        response = Response(
            detail="updated user information"
        )
        return JSONResponse(
            response.model_dump(),
            status.HTTP_200_OK
        )
    except InvalidId:
        raise HTTPException(422,"wrong object id form")

@router.post("/add_role/{user_id}")
async def add_role(role_data : RoleRequest,user_id = Path(...),this_user : UserBase = Depends(get_user)):
    try:
        if not this_user:
            response = Response(
                detail="unauthorize user"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_401_UNAUTHORIZED,
            )
        role = await retrieve_filter(roles,{"role_name" : role_data.role_name})
        role = RoleBase.model_validate(role[0])
        action = await retrieve_filter(actions,{"action_name" : "create"})
        action = ActionBase.model_validate(action[0])
        resource = await retrieve_filter(resources,{"resource_name" : "role_user"})
        resource = ResourceBase.model_validate(resource[0])
        user = await retrieve_filter(users,{"_id" : ObjectId(user_id)})
        if not user:
            raise HTTPException(404,"user does not exist")
        user = UserBase.model_validate(user[0])
        check_role = await role_base(this_user,action,resource,this_user.user_id == user.create_id)
        if check_role == False:
            response = Response(
                detail="user does not have permission"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_403_FORBIDDEN,
            )
        role_user = RoleUser(role_id=role.role_id,user_id=user_id)
        data = {
            "role_id" : ObjectId(role_user.role_id),
            "user_id" : ObjectId(role_user.user_id)
        }
        if await retrieve_filter(roles_users,data):
            raise HTTPException(422,"this user already has this role")
        await create(roles_users,data)
        response = Response(
            detail="add user role"
        )
        return JSONResponse(
            response.model_dump(),
            status.HTTP_200_OK
        )
    except InvalidId:
        raise HTTPException(422,"wrong object id form")
    
@router.delete("/delete_role/{user_id}")
async def delete_role(role_data : RoleRequest,user_id = Path(...),this_user : UserBase = Depends(get_user)):
    try:
        if not this_user:
            response = Response(
                detail="unauthorize user"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_401_UNAUTHORIZED,
            )
        role = await retrieve_filter(roles,{"role_name" : role_data.role_name})
        role = RoleBase.model_validate(role[0])
        action = await retrieve_filter(actions,{"action_name" : "delete"})
        action = ActionBase.model_validate(action[0])
        resource = await retrieve_filter(resources,{"resource_name" : "role_user"})
        resource = ResourceBase.model_validate(resource[0])
        user = await retrieve_filter(users,{"_id" : ObjectId(user_id)})
        if not user:
            raise HTTPException(404,"user does not exist")
        user = UserBase.model_validate(user[0])
        check_role = await role_base(this_user,action,resource,this_user.user_id == user.create_id)
        if check_role == False:
            response = Response(
                detail="user does not have permission"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_403_FORBIDDEN,
            )
        role_user = await retrieve_filter(roles_users,{"role_id" : ObjectId(role.role_id),"user_id" : ObjectId(user.user_id)})
        if not role_user:
            raise HTTPException(404,"this user does not have this role")
        role_user = RoleUser.model_validate(role_user[0])
        await delete(roles_users,ObjectId(role_user.role_user_id))
        response = Response(
            detail="delete user role"
        )
        return JSONResponse(
            response.model_dump(),
            status.HTTP_200_OK
        )
    except InvalidId:
        raise HTTPException(422,"wrong object id form")