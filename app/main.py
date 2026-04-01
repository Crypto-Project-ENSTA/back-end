# TODO: Keep minimal setup for now; extend when implementing routers
from fastapi import FastAPI
from app.routers import voting_system_config_router

app = FastAPI()

app.include_router(voting_system_config_router.router)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
