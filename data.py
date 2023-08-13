import pythonping
import csv
import os
from datetime import datetime

WEBSITE_FILE = "user_websites.csv"


# принимает URL сайта и выполняет к нему пинг
def ping_website(url):
    try:
        # Пингуем сайт 4 раза (по умолчанию) и возвращаем результат
        response = pythonping.ping(url, count=4)
        return response.success(), response.rtt_avg_ms
    except Exception as e:
        return False, f"Ошибка сети: {e}"


# Функция для сохранения результатов пинга. Для каждого пользователя будем создавать отдельный файл.
def save_ping_result(user_id, url, success, response_time):
    try:
        filename = f"user_{user_id}.csv"

        # Проверяем, существует ли файл
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Если файл не существовал, создаем заголовок
            if not file_exists:
                writer.writerow(["URL", "Date", "Success", "Response_Time"])

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([url, current_time, success, response_time])
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")


# Функции для чтения последних 5 результатов
def get_last_5_results(user_id):
    try:
        filename = f"user_{user_id}.csv"

        if not os.path.isfile(filename):
            return []

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            # Пропускаем заголовок и читаем все строки
            rows = list(reader)[1:]

        # Возвращаем последние 5 строк
        return rows[-5:]
    except Exception as e:
        print(f"Ошибка при получении последних 5 результатов: {e}")
        return []


# Устанавливаем сайт для пользователя и сохраняем в файле.
def set_website(user_id, website):
    try:
        websites = {}

        # Сначала загружаем все записи
        if os.path.isfile(WEBSITE_FILE):
            with open(WEBSITE_FILE, 'r') as csvfile:
                reader = csv.reader(csvfile)
                # Для каждой строки (row) в CSV-файле, мы добавляем или обновляем запись в словаре websites,
                # где ключом является user_id, а значением — URL сайта.
                for row in reader:
                    websites[row[0]] = row[1]

        # Заменяем или добавляем запись для пользователя
        websites[str(user_id)] = website

        # Записываем обратно в файл
        with open(WEBSITE_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for uid, web in websites.items():
                writer.writerow([uid, web])
    except Exception as e:
        print(f"Ошибка при добавлении web-сайта: {e}")


# Получаем сайт, который установил пользователь из файла.
def get_website(user_id):
    try:
        if not os.path.isfile(WEBSITE_FILE):
            return None

        with open(WEBSITE_FILE, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if str(user_id) == row[0]:
                    return row[1]
        return None
    except Exception as e:
        print(f"Ошибка при получении web-сайта: {e}")
        return None
