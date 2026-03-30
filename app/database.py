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
from sqlalchemy.orm import declarative_base
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
    enigne = create_engine(settings.DATABASE_URL,pool_pre_ping = True)
    
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

<<<<<<< HEAD

=======
>>>>>>> 5e13da6 ([03/30/2026 12:07:13] feat/models : implement all ORM models)
