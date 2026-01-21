from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends, status
from models.users import User 
from database import get_db
from sqlalchemy.orm import Session
from auth import get_current_user_payload


router = APIRouter(
    prefix="/account",
    tags=["account"]
)


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_my_account(
        current_user_payload: dict = Depends(get_current_user_payload),
        db: Session = Depends(get_db)) -> dict:
    
    user_id = current_user_payload["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    

    users_lectures = []
    for lect in user.lectures:
        users_lectures.append({
            "id": lect.id,
            "name": lect.name,
            "topic": lect.topic,
            "created_at": lect.created_at
        })

    return {
                "id": user.id,
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "group": user.group,
                "created_at": user.created_at,
                "lectures": users_lectures
                }
    
