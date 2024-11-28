


from TodoApp.database import Base
from sqlalchemy import Column, ForeignKey,String,Integer,Boolean



class Users(Base):
    __tablename__='users'

    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True)
    username=Column(String,unique=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    is_active=Column(Boolean,default=True)
    role=Column(String)
    phone_number=Column(String)

class Todos(Base):
    __tablename__= "todos"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    complete=Column(Boolean)
    owner_id=Column(String,ForeignKey("users.id"))