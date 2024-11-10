from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from routes.users import router as user_router
from routes.tasks import router as task_router
from fastapi.exceptions import RequestValidationError
app = FastAPI()
@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []
    for error in errors:
        formatted_errors.append({
            "error": error.get("msg"),
          
        })
    return JSONResponse(
        status_code=422,
        content=formatted_errors
    )
app.include_router(user_router,prefix="/user",tags=["user"])
app.include_router(task_router,prefix="/task",tags=["task"])
