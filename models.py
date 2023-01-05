from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User():
    def __init__(self, username, email, password, super_user=0, hash=None):
        self.username = username
        self.email = email
        if hash:
            self.password_hash = hash 
        else:
            self.set_password(password)
        self.date_joined = datetime.utcnow().timestamp() #datetime object
        self.super_user = super_user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)