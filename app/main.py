# TODO: Keep minimal setup for now; extend when implementing routers
from fastapi import FastAPI
from app.routers import voting_system_config_router
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Import all ORM models so that SQLAlchemy knows about them
# Required for Base.metadata.create_all(bind=engine) to create tables in the database
from app.models.voter import Voter
from app.models.votes import Vote
from app.models.credentials import Credential
from app.models.counted_votes import CountedVote

from app.database import Base, engine
from contextlib import asynccontextmanager


"""
Lifespan event handler for FastAPI application.

This async context manager handles application startup and shutdown events.

Startup (before yield):
- Creates all database tables defined in SQLAlchemy ORM models if they do not already exist.
- Prints a confirmation message for debugging.

Shutdown (after yield):
- Runs any cleanup code needed when the application stops (currently prints a shutdown message).

This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown") methods.
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Database tables created or already exist!")
    yield
    print("App shutdown complete!")
    
app = FastAPI(lifespan=lifespan)

app.include_router(voting_system_config_router.router)

# Allow the frontend to communicate with this API from a different domain.
# Without this, the browser blocks all cross-origin requests by default.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # list of allowed frontend URLs
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
