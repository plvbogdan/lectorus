from fastapi import APIRouter, HTTPException, Depends, status, Form, Response
from app.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.models.users import User
from passlib.context import CryptContext
from app.auth import encode_jwt
import re



router = APIRouter(
    prefix="/auth",
    tags=["auth"]

)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up(db: Session = Depends(get_db),
                  email: str = Form(..., min_length=1, max_length=100),
                  firstname: str = Form(..., min_length=1, max_length=100),
                  lastname: str = Form(..., min_length=1, max_length=100),
                  group: str = Form(..., min_length=1, max_length=100),
                  password: str = Form(..., min_length=8)
                  ) -> dict:
    if not bool(re.match(r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$', email)):
    
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Некорректный email")
    
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Данный email уже зарегистрирован")
    
    new_user = User(
        email = email,
        firstname = firstname.capitalize(),
        lastname = lastname.capitalize(),
        group = group,
        hashed_password = pwd_context.hash(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = {
            "message": "Created",
            "data" : {
            "id" : new_user.id,
            "firstname" : new_user.firstname,
            "lastname" : new_user.lastname,
            "group" : new_user.group
            }
        }
    
    return response



@router.post("/signin", status_code=status.HTTP_200_OK)
async def sign_in(
                response: Response,    
                db: Session = Depends(get_db),
                email: str = Form(..., min_length=1, max_length=100),
                password: str = Form(..., min_length=8),
                ) -> dict:
    
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный email")
    
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль")
    
    token = encode_jwt(user.id, user.email)
    if not token:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ошибка генерации токена")
    
    return {"access_token": token,
            "token_type": "Bearer"}
    