from pydantic_settings import BaseSettings
from pydantic import SecretStr
import os
import logging


def setup_logging():
    """Initializing logging settings"""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        filename='bot_logs.log',
        filemode='a'
    )


class Settings(BaseSettings):
    """Class for loading configuration data"""
    API_ID: SecretStr
    API_HASH: SecretStr
    BOT_TOKEN: SecretStr

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        env_file_encoding = 'utf-8'
