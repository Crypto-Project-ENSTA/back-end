# TODO: Keep minimal setup for now; extend when implementing routers
from fastapi import FastAPI
from app.routers import voting_system_config_router
from fastapi.middleware.cors import CORSMiddleware
from config import settings
app = FastAPI()

app.include_router(voting_system_config_router.router)

# Allow the frontend to communicate with this API from a different domain.
# Without this, the browser blocks all cross-origin requests by default.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # list of allowed frontend URLs
    allow_credentials=True,                  # allow cookies and JWT tokens
    allow_methods=["*"],                     # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                     # allow all headers (Authorization, etc.)
)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
