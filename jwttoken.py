from time import time
from config import Config
import jwt
from models import User

def get_reset_password_token(id, expires_in=1200):
    return jwt.encode(
        {'reset_password': id, 'exp': time() + expires_in},
        Config.SECRET_KEY, algorithm='HS256')

def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.get_user_by_id(int(id))
