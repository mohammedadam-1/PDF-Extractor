from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALLOWED_ORIGINS: str = Field(default="http://localhost:5173/", validation_alias="ALLOWED_ORIGINS")
    
    
    @property
    def cors_allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(sep=",") if origin.strip()]
    
    class Config:
        env_file = ".env"
        
        
        
settings = Settings()        