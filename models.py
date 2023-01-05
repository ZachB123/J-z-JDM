from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from database import db
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, email, password, super_user=0, time=None, hash=False, id=-1):
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
        self.id = id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_id(id):
        u = db.get_user_by_id((id,))
        if len(u) > 0:
            u = u[0]
            return User.user_from_tuple(u)
        return None

    @staticmethod
    def get_by_username(username):
        u = db.get_user_by_username((username,))
        if len(u) > 0:
            u = u[0]
            return User.user_from_tuple(u)
        return None

    def __str__(self) -> str:
        return f"<Id: {self.id}, Username: {self.username}, Email: {self.email}, Date Joined: {datetime.fromtimestamp(self.date_joined)}, Super User: {self.super_user}>"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def user_from_tuple(u):
        #format expected is (id, username, email, date_joined, hash, super_user)
        return User(u[1], u[2], u[4], u[5], u[3], True, u[0])

    @staticmethod
    def users_from_list(list):
        return [User.user_from_tuple(u) for u in list]

