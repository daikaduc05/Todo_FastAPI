from fastapi import FastAPI
from routes.users import router as user_router
from routes.tasks import router as task_router
app = FastAPI()

app.include_router(user_router,prefix="/user",tags=["user"])
app.include_router(task_router,prefix="/task",tags=["task"])