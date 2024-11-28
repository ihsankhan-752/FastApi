






import logging
from fastapi import Depends, APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from typing import Annotated
from TodoApp.database import SessionLocal
from TodoApp.models import Todos
from pydantic import BaseModel,Field
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()


db_dependency= Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


@router.get("/todo")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    try:
        todos = db.query(Todos).all()
        return todos
    except Exception as e:
        logging.error("Error in /admin/todo endpoint", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching todos")


@router.delete("/todo/{todo_id}")
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    todo=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo is None:
        raise HTTPException(status_code=401,detail="Todo Not Found!!")
    
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()

