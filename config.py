import os
from dotenv import load_dotenv

load_dotenv(os.path.join(".env"))

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

TELEGRAM_BOT_API_TOKEN = os.environ.get("TELEGRAM_BOT_API_TOKEN")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

GROUP = os.environ.get("GROUP")
BOT_URL = os.environ.get("BOT_URL")
