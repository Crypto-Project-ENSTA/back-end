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
from pydantic_settings import BaseSettings
from pydantic import field_validator

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
    ALLOWED_ORIGINS: list[str] # Pydantic automatically splits by comma
    DATABASE_URL: str
    
    # @field_validator: a Pydantic decorator that runs this function on the ALLOWED_ORIGINS field
    # mode="before": runs BEFORE Pydantic validates the type, so we can transform the raw value first
    @field_validator("ALLOWED_ORIGINS", mode="before")
    # @classmethod: makes this a class-level method because Pydantic calls it on the class, not an instance
    @classmethod
    # cls: refers to the Settings class itself (like 'self' but for the class)
    # v: the raw value coming from the environment variable (a plain string)
    def parse_allowed_origins(cls, v):
        # check if the value is a string (e.g. "http://localhost:3000,https://evoting-dev.vercel.app")
        if isinstance(v, str):
            # split by comma → ["http://localhost:3000", "https://evoting-dev.vercel.app"]
            # .strip() removes any accidental spaces around each URL
            return [origin.strip() for origin in v.split(",")]
        # if v is already a list, return it as-is without any transformation
        return v
    
settings=Settings()