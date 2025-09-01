from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These variables will be loaded from the .env file
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    class Config:
        # This tells pydantic to load the variables from a file named .env
        env_file = ".env"

# Create a single instance of the settings to be imported in other files
settings = Settings()