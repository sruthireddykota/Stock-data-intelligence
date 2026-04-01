from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_URL:str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings =Settings()