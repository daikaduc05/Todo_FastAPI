from fastapi import APIRouter,Body,HTTPException,Depends,status,Path
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from bson.errors import InvalidId
from schema.tasks import(
    TaskCreateRequest,
    TaskBase,
    TaskUpdateRequest

)
from schema.users import(
    UserBase
)
from db.database import(
    create,
    update,
    retrieve_all,
    retrieve_filter,
    delete,
    tasks,
    actions,
    resources
)
from service.authenticate import(
    get_user
)
from service.authorize import(
    role_base
)
from service.validate import validict
from schema.actions import ActionBase
from schema.resources import ResourceBase
from schema.response import Response
router = APIRouter()

@router.post("/todo_post/")
async def post_todo(task_data : TaskCreateRequest = Body(...),this_user : UserBase = Depends(get_user)):
    if not this_user:
            response = Response(
                detail="unauthorize user"
            )
            return JSONResponse(response.model_dump(),
                status.HTTP_401_UNAUTHORIZED,
            )
    action = await retrieve_filter(actions,{"action_name" : "create"})
    action = ActionBase.model_validate(action[0])
    resource = await retrieve_filter(resources,{"resource_name" : "task"})
    resource = ResourceBase.model_validate(resource[0])
    if await role_base(this_user,action,resource,True) == False:
          raise HTTPException(403,"user does not have permission")
    task = TaskBase(description=task_data.description,status=task_data.status,due_to=task_data.due_to,user_id=this_user.user_id,public=task_data.public,share_with=task_data.share_with)
    task = task.model_dump()
    task["user_id"] = ObjectId(task["user_id"])
    task = validict(task)
    task = await create(tasks,task)
    task = TaskBase.model_validate(task)
    return task

@router.patch("/todo_update/{task_id}")
async def update_todo(task_id : str = Path(...),task_data : TaskUpdateRequest = Body(...),this_user : UserBase = Depends(get_user)):
    try:
        if not this_user:
                response = Response(
                    detail="unauthorize user"
                )
                return JSONResponse(response.model_dump(),
                    status.HTTP_401_UNAUTHORIZED,
                )
        action = await retrieve_filter(actions,{"action_name" : "update"})
        action = ActionBase.model_validate(action[0])
        resource = await retrieve_filter(resources,{"resource_name" : "task"})
        resource = ResourceBase.model_validate(resource[0])
        task = await retrieve_filter(tasks,{"_id" : ObjectId(task_id)})
        if not task:
            raise HTTPException(404,"task does not exist")
        task = TaskBase.model_validate(task[0])
        if await role_base(this_user,action,resource,task.user_id == this_user.user_id) == False:
            raise HTTPException(403,"user does not have permission")
        task_data = TaskUpdateRequest.model_dump(task_data)
        task_data = validict(task_data)
        if "user_id" in task_data:
            task_data["user_id"] = ObjectId(task_data["user_id"])
        await update(tasks,ObjectId(task.task_id),task_data)
        response = Response(
                    detail="updated task"
        )
        return JSONResponse(response.model_dump(),
                    status.HTTP_200_OK,
        )
    except InvalidId:
         raise HTTPException(422,"wrong object id form")

    
@router.delete("/todo_update/{task_id}")
async def delete_todo(task_id : str = Path(...),this_user : UserBase = Depends(get_user)):
    try:
        if not this_user:
                response = Response(
                    detail="unauthorize user"
                )
                return JSONResponse(response.model_dump(),
                    status.HTTP_401_UNAUTHORIZED,
                )
        action = await retrieve_filter(actions,{"action_name" : "delete"})
        action = ActionBase.model_validate(action[0])
        resource = await retrieve_filter(resources,{"resource_name" : "task"})
        resource = ResourceBase.model_validate(resource[0])
        task = await retrieve_filter(tasks,{"_id" : ObjectId(task_id)})
        if not task:
            raise HTTPException(404,"task does not exist")
        task = TaskBase.model_validate(task[0])
        if await role_base(this_user,action,resource,task.user_id == this_user.user_id) == False:
            raise HTTPException(403,"user does not have permission")
        await delete(tasks,ObjectId(task.task_id))
        response = Response(
                    detail="deleted task"
        )
        return JSONResponse(response.model_dump(),
                    status.HTTP_200_OK,
        )
    except InvalidId:
         raise HTTPException(422,"wrong object id form")

@router.get("/todo_retrieve/{task_id}")
async def retrieve_todo(task_id : str = Path(...),this_user : UserBase = Depends(get_user)):
    try:
        if not this_user:
                response = Response(
                    detail="unauthorize user"
                )
                return JSONResponse(response.model_dump(),
                    status.HTTP_401_UNAUTHORIZED,
                )
        action = await retrieve_filter(actions,{"action_name" : "retrieve"})
        action = ActionBase.model_validate(action[0])
        resource = await retrieve_filter(resources,{"resource_name" : "task"})
        resource = ResourceBase.model_validate(resource[0])
        task = await retrieve_filter(tasks,{"_id" : ObjectId(task_id)})
        if not task:
            raise HTTPException(404,"task does not exist")
        task = TaskBase.model_validate(task[0])
        if await role_base(this_user,action,resource,task.user_id == this_user.user_id) == False:
            if not this_user.user_id in task.share_with:
                if task.public == False:
                    raise HTTPException(403,"user does not have permission")
        return task
    except InvalidId:
         raise HTTPException(422,"wrong object id form")
