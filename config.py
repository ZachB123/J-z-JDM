import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    TEMPLATES_AUTO_RELOAD = True,
    SECRET_KEY = os.environ.get("SECRET_KEY")