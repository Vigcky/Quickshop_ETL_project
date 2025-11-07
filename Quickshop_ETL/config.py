from pydantic import BaseSettings

class Settings(BaseSettings):
    input_dir: str = "data"
    output_dir: str = "out"
    db_url: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
