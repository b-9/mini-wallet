from dotenv import load_dotenv
import os

load_dotenv()

BASE_ROUTER = os.getenv("BASE_ROUTER","")

DB_USER = os.environ["DB_USER"]
DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]


DB_CONFIG = {
    "DB_USER": DB_USER,
    "DB_NAME": DB_NAME,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
}
