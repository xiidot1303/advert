import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(os.path.join('.env'))

TELEGRAM_BOT_API_TOKEN=os.environ.get('TELEGRAM_BOT_API_TOKEN')
ENVIRONMENT=os.environ.get('ENVIRONMENT')

DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
GROUP = os.environ.get('GROUP')
BOT_URL=os.environ.get('BOT_URL')
CLICK_SERVICE_ID=os.environ.get('CLICK_SERVICE_ID')
CLICK_MERCHANT_ID=os.environ.get('CLICK_MERCHANT_ID')
CLICK_SECRET_KEY=os.environ.get('CLICK_SECRET_KEY')
CLICK_MERCHANT_USER_ID=os.environ.get('CLICK_MERCHANT_USER_ID')
