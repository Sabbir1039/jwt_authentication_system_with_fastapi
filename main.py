from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .models import User, Base
from .schemas import UserCreateSchema, UserResponseSchema, UserUpdateSchema, TokenSchema
from .database import engine, SessionLocal
from .deps import get_current_user
from .utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from uuid import uuid4

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/signup', summary="Create new user", response_model=UserResponseSchema)
async def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = db.query(User).filter(User.email == data.email).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    password = get_hashed_password(data.password)

    new_user = User(name=data.name, email=data.email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.name == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
        "token_type": "bearer"
    }
    
@app.get('/me', summary='Get details of currently logged in user', response_model=UserResponseSchema)
async def get_me(user: User = Depends(get_current_user)):
    return user

    
@app.get("/users/{user_id}", response_model=UserResponseSchema)
async def get_users(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    
    except Exception as e:
        return {"error": e}