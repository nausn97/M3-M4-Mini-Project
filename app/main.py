from fastapi import FastAPI
from starlette import status
from core import core
from auth import auth
from database import Base, engine, SessionLocal

app = FastAPI()

app.include_router(core.router, prefix="/api", tags=["core-api"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])

Base.metadata.create_all(bind=engine)

@app.get("/healthy", status_code=status.HTTP_200_OK)
def health():
    return {"message": "The system is healthy"}