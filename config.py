# config.py
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    xero_api_base_url: str = os.getenv('XERO_API_BASE_URL', 'http://localhost:3000')


settings = Settings()
