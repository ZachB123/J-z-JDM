import os
from dotenv import load_dotenv
load_dotenv()

# Configuration for the app
class Config(object):
    TEMPLATES_AUTO_RELOAD = True,
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_USER = os.environ.get("DATABASE_USER") 
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE = os.environ.get("DATABASE")
    CARS_PER_PAGE = 15
    CACHE_TYPE = "FileSystemCache"
    CACHE_DIR = "/cache"
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    MAIL_SENDGRID_API_KEY = os.environ.get("MAIL_SENDGRID_API_KEY")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
