import pythonping
import csv
import os
from datetime import datetime
from urllib.parse import urlparse
from config import setup_logging
import logging


WEBSITE_FILE = "user_websites.csv"

setup_logging()


def ping_website(url):
    """takes a website URL and pings it"""
    try:
        domain_name = urlparse(url).netloc
        response = pythonping.ping(domain_name, count=4)
        return response.success(), response.rtt_avg_ms
    except Exception as e:
        logging.error(f"Website ping error {url}: {e}")
        return False, f"Ошибка сети: {e}"


def save_ping_result(user_id, url, success, response_time):
    """function for saving ping results. We will create a separate file for each user"""
    try:
        filename = f"user_{user_id}.csv"

        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(["URL", "Date", "Success", "Response_Time"])

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([url, current_time, success, response_time])
        logging.info(f"Ping results for user {user_id} и URL {url}  saved.")
    except Exception as e:
        logging.error(f"Error saving ping results: {e}")


def get_last_5_results(user_id):
    """functions for reading the last 5 results"""
    try:
        filename = f"user_{user_id}.csv"

        if not os.path.isfile(filename):
            return []

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)[1:]

        return rows[-5:]
    except Exception as e:
        logging.error(f"Error getting last 5 results: {e}")
        return []


def set_website(user_id, website):
    """saving a user's site"""
    try:
        websites = {}

        if os.path.isfile(WEBSITE_FILE):
            with open(WEBSITE_FILE, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    websites[row[0]] = row[1]

        websites[str(user_id)] = website

        with open(WEBSITE_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for uid, web in websites.items():
                writer.writerow([uid, web])
        logging.info(f"Added site {website} for user {user_id}.")
    except Exception as e:
        logging.error(f"Error adding site for user {user_id}: {e}")


def is_user(user_id):
    """checks if a user record exists"""
    try:
        if not os.path.exists("user_websites.csv"):
            create_users_main_file()

        with open("user_websites.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id:
                    return True
        return False
    except Exception as e:
        print(f"Error checking if user exists: {e}")


def create_users_main_file():
    """creates a new CSV file if it doesn't exist"""
    try:
        with open("user_websites.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "website"])
        logging.info("user_websites.csv file created successfully.")
    except Exception as e:
        logging.error(f"Error creating file user_websites.csv: {e}")


def save_user_without_website(user_id):
    """saves the user ID to a file without specifying a website"""
    try:
        with open("user_websites.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, ''])
        logging.info(f"User ID {user_id} saved successfully without a website.")
    except Exception as e:
        logging.error(f"Error saving user_id {user_id} without specifying a website: {e}")


def get_all_users_websites():
    """returns a dictionary with user_id and their sites"""
    websites = {}

    try:
        if not os.path.isfile(WEBSITE_FILE):
            return websites

        with open(WEBSITE_FILE, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1]:  # проверка, что URL сайта указан
                    websites[row[0]] = row[1]
    except Exception as e:
        logging.error(f"error while reading file {WEBSITE_FILE}: {e}")

    return websites

