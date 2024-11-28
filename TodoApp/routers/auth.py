from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from TodoApp.models import Users 
from TodoApp.database import SessionLocal
from sqlalchemy.orm import Session

from passlib.context import CryptContext   #using for hashing password 

from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer   #for signIn provide its own username and password

from jose import jwt,JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY="NnqRebqOjOid500BFMaaAqJu9rdv2T9MG_n3c8swQSaMiui8fb5dBe-It7-OQwYqgWjJe3rCKP5B9MRY_PjLag"
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')   # every api endpoint will be rely on this first user will signin to validate token


class UserRequestModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token:str
    token_type:str


def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()


db_dependency= Annotated[Session,Depends(get_db)]


def authenticate_user(username: str, password:str,db):
    user=db.query(Users).filter(Users.username==username).first()    #here we check username which already exist
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):      #here we check hashed password which is exist in DB
        return False
    return user


def create_access_token(username:str, user_id:int,role:str,expire_delta:timedelta):
    encode={'sub':username,'id':user_id,'role':role}    #act as a payload
    expires=datetime.now(timezone.utc) + expire_delta  # for expiry of token
    encode.update({'exp': expires})

    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)  #user to create token


def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    #each Todo need security thats why we will call this function first
    #to verify the token which is getting from user

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])  # here we decode our token
        username :str =payload.get('sub')
        user_id:int =payload.get('id')
        user_role:str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=401,detail="Credentials not validate")
        

        return {'username':username,'id':user_id,'user_role':user_role}
    
    except JWTError:
         raise HTTPException(status_code=401,detail="Credentials not validate")
    


@router.get("/user")
async def get_user(current_user: Annotated[dict, Depends(get_current_user)], db: db_dependency):
    user = db.query(Users).filter(Users.id == current_user['id']).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

    


@router.post("/auth", response_model=Token)
async def create_user(db: db_dependency, create_user_request: UserRequestModel):
    try:
        create_user_model = Users(
            username=create_user_request.username,
            email=create_user_request.email,
            first_name=create_user_request.first_name,
            last_name=create_user_request.last_name,
            hashed_password=bcrypt_context.hash(create_user_request.password),
            role=create_user_request.role,
            is_active=True
        )

        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model) 

        token=create_access_token(
            username=create_user_model.username,
            user_id=create_user_model.id,
            expire_delta=timedelta(minutes=30),
            role=create_user_model.role
        )
        
        return {"access_token": token,'token_type':"bearer"}  
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


    

    
@router.post("/token",response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401,detail="Could not validate user")

    token=create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    
    return {'access_token':token, 'token_type':'bearer'}
    
