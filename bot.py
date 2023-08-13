import validators
from pyrogram import Client, filters
from data import set_website, get_website, ping_website, save_ping_result, get_last_5_results
from config import Settings

config = Settings()

app = Client("my_bot", api_id=int(config.API_ID), api_hash=config.API_HASH.get_secret_value(),
             bot_token=config.BOT_TOKEN.get_secret_value())


# декоратор указывает, что функция (start()) будет вызвана, когда бот получает сообщение с командой "/start".
@app.on_message(filters.command("start"))
def start(client, message):
    # метод объекта message, который позволяет боту ответить на полученное сообщение с определенным текстом.
    message.reply_text("Привет! Введите адрес сайта, "
                       "который вы хотите отслеживать с помощью команды /set <адрес_сайта>.")


@app.on_message(filters.command("set"))
def set_url(client, message):
    # проверяет количество элементов в списке message.command
    if len(message.command) < 2:
        message.reply_text("Пожалуйста, укажите URL сайта после команды /set.")
        return

    url = message.command[1]
    url = url.strip()

    if not url.startswith(("http://", "https://", "www.")):
        url = "http://" + url  # Добавляем протокол по умолчанию, если он отсутствует
    elif url.startswith("www."):
        url = "http://" + url  # Добавляем протокол к URL, начинающемуся с www.

    # валидация url-а
    if not validators.url(url):
        message.reply_text(f"'{url}' не является действительным URL. Попробуйте снова.")
        return

    set_website(message.from_user.id, url)
    message.reply_text(f"URL {url} установлен для отслеживания!")


@app.on_message(filters.command("list"))
def get_list(client, message):
    results = get_last_5_results(message.from_user.id)
    if not results:
        message.reply_text("Нет результатов для отображения.")
        return

    response_text = "Последние 5 результатов:\n"
    for row in results:
        response_text += f"{row[1]} - {row[2]} - {row[3]} ms\n"
    message.reply_text(response_text)


if __name__ == "__main__":
    app.run()
