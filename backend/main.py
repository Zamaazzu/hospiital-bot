from fastapi import FastAPI
from db.database import engine, Base

# Import all models
from db.models import *

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hospital OP Bot API Running"}



Base.metadata.create_all(bind=engine)