import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')


load_dotenv()
# FOR TELEGRAM_API
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN_STM')

