"""
config.py

This file handles the project configuration and environment settings.
It includes critical settings such as:
- DATABASE_URL: the database connection string
- Security-related configurations like hashing algorithms or JWT settings (if used)
- Any other global configuration variables needed throughout the application

Using Pydantic's BaseSettings allows these values to be loaded from environment variables,
making the project easy to configure for different environments (development, testing, production).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # We inherit from Pydantic's BaseSettings so that each class 
    # attribute automatically maps to an environment variable. 

    # Benefits:
    # - Centralized configuration for the project
    # - Automatic type validation (e.g., DATABASE_URL must be a string)
    # - Easy switching between environments (development, testing, production)
    # - No need to manually parse or load env variables

    # In short, inheritance allows us to treat environment variables as
    # typed Python attributes while keeping the code clean and maintainable.
    
    ENV: str
    ALLOWED_ORIGINS: str
    DATABASE_URL: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings=Settings()