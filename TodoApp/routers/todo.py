
from fastapi import Depends, APIRouter,HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from TodoApp.database import SessionLocal
from TodoApp.models import Todos
from pydantic import BaseModel,Field
from .auth import get_current_user

router = APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()


db_dependency= Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3, max_length=100)
    priority: int
    complete:bool



@router.get("/")
async def get_all_todos(db: db_dependency):
    
    
    return db.query(Todos).all()





@router.get("/todo/{todo_id}")
async def get_todo_by_id(user:user_dependency,db:db_dependency,todo_id:int):
    if user is None:
        raise HTTPException(status_code=401,detail="User Not Found")
    
    todo=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get("id")).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404,detail="Todo Not Found")



@router.post("/create_todo")
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="User Not Found")

    todo = Todos(
        title=todo_request.title,
        description=todo_request.description,
        priority=todo_request.priority,
        complete=todo_request.complete,
        owner_id=user.get('id')
    )
    try:
        db.add(todo)
        db.commit()
        db.refresh(todo)  
        return {"message": "Todo created successfully", "todo": todo}
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")  
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")




@router.put("/update_todo/{todo_id}")
async def update_todo(user:user_dependency,db:db_dependency,todo_id:int,todo_request:TodoRequest):


    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")


    todo=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="No Todo Found for update")
    todo.title=todo_request.title
    todo.description=todo_request.description
   

    db.add(todo)
    db.commit()




@router.delete("/delete_todo/{todo_id}")
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int):
    if user is None:
        raise HTTPException(status_code=401,detail="User Not authenticated")
    
    todo=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()
    db.commit()
    

