from pydantic import BaseSettings, SecretStr
import os


class Settings(BaseSettings):
    API_ID: SecretStr
    API_HASH: SecretStr
    BOT_TOKEN: SecretStr

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        env_file_encoding = 'utf-8'
