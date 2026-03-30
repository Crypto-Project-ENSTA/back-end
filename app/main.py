# TODO: Keep minimal setup for now; extend when implementing routers
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

from app.init_db import init_db

init_db()