from fastapi import FastAPI
from app.routers import lectures, users, auth
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

#Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Лекторус",
    version="0.1.0"
)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(lectures.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в Лекторус"}