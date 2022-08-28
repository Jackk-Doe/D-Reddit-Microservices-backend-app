from os import getenv
from dotenv import load_dotenv

load_dotenv()

PORT = getenv('PORT')
POST_SERVICES_URL = getenv('POST_SERVICES_URL')
USER_SERVICES_URL = getenv('USER_SERVICES_URL')