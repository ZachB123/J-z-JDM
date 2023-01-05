from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from database import db

class User():
    def __init__(self, username, email, password, super_user=0, time=None, hash=False):
        self.username = username
        self.email = email
        if hash:
            self.password_hash = password 
        else:
            self.set_password(password)
        if time:
            self.date_joined = time
        else:
            self.date_joined = datetime.utcnow().timestamp() #datetime object
        self.super_user = super_user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def get_user_by_id(id):
    u = db.get_user_by_id((id,))
    if len(u) > 0:
        u = u[0]
        return User(u[1], u[2], u[4], u[5], u[3], True)
    return None