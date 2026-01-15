from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends, status
from app.models.users import User 
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)) -> dict:
    db_users = db.query(User).order_by(User.created_at).all()
    all_users = {}
    for user in db_users:
        group = user.group
        all_users.setdefault(group, []).append({
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "created_at": user.created_at,
        "count_lectures": len(user.lectures)
        })
    
    return all_users


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)) -> dict:
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
