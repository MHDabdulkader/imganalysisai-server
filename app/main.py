from fastapi import FastAPI
from app.router.user_router import router as user_router
from app.router.token_router import router as token_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My FastAPI Project")

# routers
app.include_router(user_router)
app.include_router(token_router)