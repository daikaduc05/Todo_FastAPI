from fastapi import APIRouter,Body,HTTPException,Depends,status,Path
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schema.tasks import(
    TaskCreateRequest,
    TaskUpdateRequest
)
from db.database import(
    create,
    update,
    retrieve_all,
    retrieve_filter,
    delete,
    tasks
)
from service.authenticate import(
    get_user,
    RoleBaseAccessControl
)
router = APIRouter()

@router.post("/todo_post/")
async def post_todo(task_data : TaskCreateRequest = Body(...),user : dict = Depends(get_user)):
    task_data = jsonable_encoder(task_data) 
    if not isinstance(user,dict):
        return user
    task_data["assigned_to"] = user["user_id"]
    newtask = await create(tasks,task_data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "action" : "post task"
        }
    )


@router.patch("/todo_update/{task_id}")
async def update_todo(task_data : TaskUpdateRequest = Body(...),
                      permission:bool = Depends(RoleBaseAccessControl(allowed_role={"admin"}, action="update"))):
    if not isinstance(permission,dict):
        return permission
    task_data = jsonable_encoder(task_data)
    await update(tasks,permission["task_id"],task_data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "action" : "update task"
        }
    )

    
@router.delete("/todo_delete/{task_id}")
async def delete_todo(permission:bool = Depends(RoleBaseAccessControl(allowed_role={"admin"}, action="delete"))):
    if not isinstance(permission,dict):
        return permission
    await delete(tasks,permission["task_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "action" : "delete task"
        }
    )
@router.get("todo_retrieve/{task_id}")
async def retrieve_todo(permission:bool = Depends(RoleBaseAccessControl(allowed_role={"admin"}, action="retrieve"))):
    if not isinstance(permission,dict):
        return permission
    task = await retrieve_filter(tasks,{"_id" : ObjectId(permission["task_id"])})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=task
    )
