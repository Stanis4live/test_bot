from pyrogram import Client, filters
from data import set_website, get_website, ping_website, save_ping_result, get_last_5_results
from config import Settings

config = Settings()

app = Client("my_bot", api_id=int(config.API_ID), api_hash=config.API_HASH.get_secret_value(), bot_token=config.BOT_TOKEN.get_secret_value())