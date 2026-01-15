from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends, status, Response, dependencies, Request
from app.database import get_db
from app.models.lectures import LectureDB
from app.parser import notebook_parser
from sqlalchemy.orm import Session
import json
from typing import Optional
from app.auth import get_current_user_payload
from app.models.users import User 

router = APIRouter(
    prefix="/lectures",
    tags=["lectures"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_lectures(db: Session = Depends(get_db)) -> list:
    db_lectures = db.query(LectureDB).order_by(LectureDB.created_at.desc()).all()
    all_lectures = []
    for lecture in db_lectures:
        all_lectures.append(
            {
                "id": lecture.id,
                "name": lecture.name,
                "topic": lecture.topic,
                "group": lecture.author.group,
                "author_firstname" : lecture.author.firstname,
                "author_lastname" : lecture.author.lastname,
                "created_at": lecture.created_at
            }
        )
    return all_lectures




@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_lecture(
    current_user_payload: dict = Depends(get_current_user_payload),
    file: UploadFile = File(...), 
    name: str = Form(..., min_length=1, max_length=250),
    topic: Optional[str] = Form(min_length=2, max_length=200),
    db: Session = Depends(get_db)):
    if not file.filename.endswith(".ipynb"):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Только .ipynb файлы")
    try:
        
        try:
            user_id = current_user_payload["user_id"]
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка авторизации")
        
        notebook = await file.read()
        notebook_json = json.loads(notebook.decode('utf-8'))
        
        user = db.query(User).filter(User.id == user_id).first()

     
        new_lecture = LectureDB(
            name = name,
            author = user,
            author_id = user_id,
            topic = topic,
            content = notebook_json
        )

        db.add(new_lecture)
        db.commit()
        db.refresh(new_lecture)

        response = {
            "message": "Created",
            "data" : {
            "id" : new_lecture.id,
            "name" : new_lecture.name,
            "group": new_lecture.author.group,
            "author_firstname" : new_lecture.author.firstname,
            "author_lastname" : new_lecture.author.lastname,
            "topic" : new_lecture.topic
            }
        }
        return response
    
    except Exception as e:  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




@router.get("/{lecture_id}", status_code=status.HTTP_200_OK)
async def get_lecture(lecture_id: int, db: Session = Depends(get_db)) -> dict:
    lecture = db.query(LectureDB).filter(LectureDB.id == lecture_id).first()
    if lecture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лекция не найдена")
    else:
        return{
            "id": lecture.id,
            "name": lecture.name,
            "group": lecture.author.group,
            "author_firstname" : lecture.author.firstname,
            "author_lastname" : lecture.author.lastname,
            "topic": lecture.topic,
            "created_at": lecture.created_at,
            "lecture": notebook_parser(lecture.content)
        }

@router.delete("/{lecture_id}", status_code=status.HTTP_200_OK)
async def delete_lecture(lecture_id: int, 
                         current_user_payload: dict = Depends(get_current_user_payload),
                         db: Session = Depends(get_db)) -> dict:
    
    lecture = db.query(LectureDB).filter(LectureDB.id == lecture_id).first()
    if lecture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лекция не найдена")
    
    try:
        user_id = current_user_payload["user_id"]
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка авторизации")
    
    if user_id == lecture.author_id:
        db.delete(lecture)
        db.commit()
        return {"message": f"Лекция {lecture_id} удалена"}
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для удаления")





