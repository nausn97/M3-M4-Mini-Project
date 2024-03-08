from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel
from starlette import status
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter()

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/signin')
SECRET_KEY = "7ee976707b585ac5635559d949d46d076df9c7c595da8715c4d856aac19d8a9f"
ALGORITHM = "HS256"
class UserCreateRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db) -> bool:
    user = db.query(Users).filter(Users.username == username).first()
    if user and bcrypt.verify(password, user.password):
        return user
    else:
        return False


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id
    }
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        id: int = payload.get('id')
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate")
        return {'username': username, 'id': id}
    except:
        raise JWTError(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, request: UserCreateRequest):
    user = Users(
        username=request.username,
        password=bcrypt.hash(request.password)
    )
    db.add(user)
    db.commit()


@router.post("/signin", response_model=Token, status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency,
                   form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Username and Password incorrect")
    token = create_access_token(form_data.username, user.id, timedelta(minutes=20))
    return {
        "access_token": token,
        "token_type": "Bearer"
    }



@router.get("/user", status_code=status.HTTP_200_OK)
def get_user(db: db_dependency):
    return db.query(Users).all()


@router.get("/user/{user_name}", status_code=status.HTTP_200_OK)
def get_user(db: db_dependency, user_name: str):
    user=db.query(Users).filter(Users.username == user_name).first()
    if user is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


