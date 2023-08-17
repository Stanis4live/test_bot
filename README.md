[Read in Russian (Читать на русском)](README_RU.md)

# Website Uptime Checker Bot

## Overview

This bot checks the uptime of websites provided by the users. It pings specified URLs and returns the results to the users.

## Features:

- Users can add or remove URLs for monitoring.
- Users receive updates when the status of a monitored URL changes.
- Logging functionality provides detailed information about bot operations.
- Settings loaded from environment variables for increased security.

## Installation and Running:

1. Clone the repository: $ git clone https://github.com/Stanis4live/test_bot.git
2. Change to the project directory: $ cd path/to/your/project
3. Create a virtual environment: $ python3 -m venv venv
4. Activate the virtual environment: $ source venv/bin/activate
(On Windows, use venv\Scripts\activate instead of source venv/bin/activate).
5. Install the required dependencies: $ pip install -r requirements.txt
6. Set up the environment variables by creating a .env file in the root directory (or exporting them in your shell). 
The required variables are: API_ID, API_HASH, and BOT_TOKEN.
7. Run the bot with the virtual environment activated: (venv) $ python bot.py

Feedback and Issues:
For feedback, suggestions, or issues, please open an issue in the GitHub repository or contact the repository owner.

