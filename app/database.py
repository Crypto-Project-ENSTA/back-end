"""
database.py

This file handles the SQLAlchemy database setup for the project. It is responsible for:
- Creating the database engine based on the environment configuration (SQLite or other DBs)
- Configuring engine options for reliability (e.g., check_same_thread for SQLite, pool_pre_ping for other DBs)
- Defining the Declarative Base class for ORM models, which is the foundation for all table mappings
- (Later) providing a session factory for database operations

In short, this file centralizes all database configuration and setup,
so that the rest of the application can interact with the database using ORM models safely and consistently.
"""

from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base,sessionmaker
from app.config import settings


isSqlite = settings.DATABASE_URL.startswith('sqlite')

#1 Create_engine
if (isSqlite==True):
    #TODO : explain why we use false in the thread checking.
    engine = create_engine(settings.DATABASE_URL,connect_args={"check_same_thread": False})
else:
    # We use `pool_pre_ping=True` to avoid broken database connections.
    # Sometimes the database closes connections (timeout, restart, etc.),
    # and using a dead connection causes errors like "connection closed".
    # This option checks if the connection is still alive before using it:
    # - If yes → use it
    # - If no → reconnect automatically
    # In short: it prevents crashes by ensuring the connection works
    engine = create_engine(settings.DATABASE_URL,pool_pre_ping = True)
    
#2 create Base class

# Declarative Base for ORM models
# We declare this so that:
# - Python classes can be mapped automatically to database tables
# - SQLAlchemy can track table metadata (columns, constraints, relationships)
# - We can use ORM features like session.add(), session.query(), and relationships
# - Shared methods or attributes can optionally be added to all models
# In short, this is the foundation for all ORM models in the project.

# Without declarative_base():
# - Python classes cannot be automatically mapped to database tables
# - SQLAlchemy cannot track table metadata or relationships
# - ORM features (session.add(), session.query(), etc.) won’t work
# - You would need to define tables manually and write raw SQL for CRUD
# In short, you lose all the conveniences of the ORM and must manage tables and queries manually.
Base = declarative_base()


"""
SessionLocal - SQLAlchemy Session Factory

This creates a factory for SQLAlchemy sessions using `sessionmaker`. Each session
represents a **workspace** for interacting with the database.

Parameters:

1. autocommit (bool)
    - Controls whether changes are **automatically saved to the database**.
    - autocommit=True  -> changes are persisted immediately (rarely used in modern FastAPI apps).
    - autocommit=False -> changes are staged in the session; must call db.commit() to save.

2. autoflush (bool)
    - Controls whether **staged changes are sent to the DB automatically before queries**.
    - autoflush=True  -> pending changes are flushed automatically, so queries see uncommitted data.
    - autoflush=False -> queries only see data already committed; staged changes remain invisible until flush or commit.
    - **Note:** autoflush ≠ commit. Flushed data is visible to queries but **not permanently saved** until commit.

3. bind
    - The database engine to connect to (created with create_engine()).

Important Notes:
    - Always use `db.commit()` to persist changes permanently.
    - Use `db.rollback()` if an error occurs to undo staged changes.
    - Use `db.close()` to release the connection after use.
    - In FastAPI, use this with a dependency function to provide `db: Session` to endpoints.

"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



"""
FastAPI Database Dependency - get_db

This function provides a database session to FastAPI endpoints using dependency injection.

It follows a generator-based pattern with `yield`, which allows FastAPI to manage
the lifecycle of the database session automatically:

- A new session is created for each request
- The session is provided to the endpoint via `yield`
- After the request finishes (success or error), the session is safely closed

Why use this pattern:
- Prevents database connection leaks
- Ensures each request has an isolated session
- Guarantees cleanup even if an exception occurs
"""
def get_db() :
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
