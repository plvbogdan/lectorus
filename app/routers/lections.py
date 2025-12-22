from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends, status
from app.database import get_db
from app.models.lections import LectionDB
from app.parser import notebook_parser
from sqlalchemy.orm import Session
import json
from typing import Optional

router = APIRouter(
    prefix="/lections",
    tags=["lections"]
)




@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_lections(db: Session = Depends(get_db)) -> list:
    db_lections = db.query(LectionDB).order_by(LectionDB.created_at.desc()).all()
    all_lections = []
    for lection in db_lections:
        all_lections.append(
            {
                "id": lection.id,
                "name": lection.name,
                "author": lection.author,
                "topic": lection.topic,
                "created_at": lection.created_at
            }
        )
    return all_lections




@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_lection(file: UploadFile = File(...), 
    name: str = Form(..., min_length=1, max_length=250),
    author: str = Form(..., min_length=1, max_length=200),
    topic: Optional[str] = Form(None, min_length=2, max_length=200),
    db: Session = Depends(get_db)) -> dict:

    if not file.filename.endswith(".ipynb"):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Только .ipynb файлы")
    try:
        notebook = await file.read()
        notebook_json = json.loads(notebook.decode('utf-8'))

        new_lection = LectionDB(
            name = name,
            author = author,
            topic = topic,
            content = notebook_json
        )

        db.add(new_lection)
        db.commit()
        db.refresh(new_lection)

        response = {
            "message": "Created",
            "data" : {
            "id" : new_lection.id,
            "name" : new_lection.name,
            "author" : new_lection.author,
            "topic" : new_lection.topic
            }
        }
        return response
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




@router.get("/{lection_id}", status_code=status.HTTP_200_OK)
async def get_lection(lection_id: int, db: Session = Depends(get_db)) -> dict:
    lection = db.query(LectionDB).filter(LectionDB.id == lection_id).first()
    if lection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лекция не найдена")
    else:
        return{
            "id": lection.id,
            "name": lection.name,
            "author": lection.author,
            "topic": lection.topic,
            "created_at"
            "lection": notebook_parser(lection.content)
        }

@router.delete("/{lection_id}", status_code=status.HTTP_200_OK)
async def delete_lection(lection_id: int, db: Session = Depends(get_db)) -> dict:
    lection= db.query(LectionDB).filter(LectionDB.id == lection_id).first()
    if lection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лекция не найдена")
    else:
        db.delete(lection)
        db.commit()
        return {"message": f"Лекция {lection_id} удалена"}


# @router.put("/{lection_id}")
# async def update_lection(lection_id: int) -> dict:
#     return {"message": f"Лекция {lection_id} обнавлена (заглушка)"}