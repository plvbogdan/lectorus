from fastapi import FastAPI
from app.routers import lectures
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Лекторус",
    version="0.1.0"
)

app.include_router(lectures.router)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в Лекторус"}