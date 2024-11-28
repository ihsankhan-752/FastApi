

from fastapi import FastAPI
import TodoApp.models
from TodoApp.database import engine
from TodoApp.routers import todo,auth,admin


app=FastAPI()

TodoApp.models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)

