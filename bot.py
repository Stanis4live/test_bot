import validators
from pyrogram import Client, filters
from data import (set_website, ping_website, save_ping_result, get_last_5_results, is_user,
                  save_user_without_website, get_all_users_websites)
from config import Settings, setup_logging
import logging
import asyncio


config = Settings()
setup_logging()

app = Client("my_bot", api_id=int(config.API_ID.get_secret_value()), api_hash=config.API_HASH.get_secret_value(),
             bot_token=config.BOT_TOKEN.get_secret_value())


@app.on_message(filters.command("start"))
def start(client, message):
    """start command processing"""
    try:
        user_id = str(message.from_user.id)

        if not is_user(user_id):
            save_user_without_website(user_id)

        message.reply_text("Привет! Вот список доступных команд:\n"
                           "/start - Запустить бота\n"
                           "/set <адрес_сайта> - Задать новый адрес сайта\n"
                           "/list - Получить последние 5 результатов для вашего адреса сайта\n"
                           "\nВведите адрес сайта, который вы хотите отслеживать с помощью команды /set <адрес_сайта>.")
        logging.info(f"User {message.from_user.id} launched the bot.")
    except Exception as e:
        logging.error(f"Error processing command start: {e}")


@app.on_message(filters.command("set"))
def set_url(client, message):
    """set command processing"""
    try:
        if len(message.command) < 2:
            message.reply_text("Пожалуйста, укажите URL сайта после команды /set.")
            return

        url = message.command[1]
        url = url.strip()

        if not url.startswith(("http://", "https://", "www.")):
            url = "http://" + url
        elif url.startswith("www."):
            url = "http://" + url

        if not validators.url(url):
            message.reply_text(f"'{url}' не является действительным URL. Попробуйте снова.")
            return

        set_website(message.from_user.id, url)
        message.reply_text(f"URL {url} установлен для отслеживания!")
        logging.info(f"URL {url} set to be tracked by the user {message.from_user.id}")
    except Exception as e:
        logging.error(f"Error setting URL: {e}")


@app.on_message(filters.command("list"))
def get_list(client, message):
    """list command processing"""
    results = get_last_5_results(message.from_user.id)
    if not results:
        message.reply_text("Нет результатов для отображения.")
        return

    response_text = "Последние 5 результатов:\n"
    for row in results:
        response_text += f"{row[1]} - {row[2]} - {row[3]} ms\n"
    message.reply_text(response_text)


async def ping_all_users():
    """pings websites of all users"""
    while True:
        try:
            user_websites = get_all_users_websites()
            for user_id, website in user_websites.items():
                success, response_time = ping_website(website)
                save_ping_result(user_id, website, success, response_time)
            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Error when pinging all users: {e}")
            await asyncio.sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(ping_all_users())
    app.run()
