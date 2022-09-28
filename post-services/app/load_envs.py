# This file is used to load datas from .env
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv('DATABASE_URL')
PORT = getenv('PORT')
USER_SERVICES_URL = getenv('USER_SERVICES_URL')
CONTENT_RECOMMEND_SERVICES_URL = getenv('CONTENT_RECOMMEND_SERVICES_URL')