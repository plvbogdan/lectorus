from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends, status
from app.database import get_db
from app.models.lectures import LectureDB
from app.parser import notebook_parser
from sqlalchemy.orm import Session
import json
from typing import Optional

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
                "author": lecture.author,
                "topic": lecture.topic,
                "created_at": lecture.created_at
            }
        )
    return all_lectures




@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_lecture(file: UploadFile = File(...), 
    name: str = Form(..., min_length=1, max_length=250),
    author: str = Form(..., min_length=1, max_length=200),
    topic: Optional[str] = Form(None, min_length=2, max_length=200),
    db: Session = Depends(get_db)) -> dict:

    if not file.filename.endswith(".ipynb"):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Только .ipynb файлы")
    try:
        notebook = await file.read()
        notebook_json = json.loads(notebook.decode('utf-8'))

        new_lecture = LectureDB(
            name = name,
            author = author,
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
            "author" : new_lecture.author,
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
            "author": lecture.author,
            "topic": lecture.topic,
            "created_at": lecture.created_at,
            "lecture": notebook_parser(lecture.content)
        }

@router.delete("/{lecture_id}", status_code=status.HTTP_200_OK)
async def delete_lecture(lecture_id: int, db: Session = Depends(get_db)) -> dict:
    lecture= db.query(LectureDB).filter(LectureDB.id == lecture_id).first()
    if lecture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лекция не найдена")
    else:
        db.delete(lecture)
        db.commit()
        return {"message": f"Лекция {lecture_id} удалена"}


# @router.put("/{lecture_id}")
# async def update_lecture(lecture_id: int) -> dict:
#     return {"message": f"Лекция {lecture_id} обнавлена (заглушка)"}