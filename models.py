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

    @staticmethod
    def add_user(user):
        db.create_user(user)


class Car():
    def __init__(self, description, oem, model, year, mileage, color, price, drivetrain, engine_cylinder, engine_size, four_wheel_steering, abs, tcs, doors, seats, horsepower, torque, misc, sales_rep_id=-1, id=-1):
        self.description = description #text
        self.oem = oem #text
        self.model = model #text
        self.year = year #number
        self.mileage = mileage #number
        self.color = color #text
        self.price = price #number
        self.drivetrain = drivetrain #text
        self.engine_cylinder = engine_cylinder #text
        self.engine_size = engine_size #number
        self.four_wheel_steering = four_wheel_steering #bool/num
        self.abs = abs #bool/num
        self.tcs = tcs #bool/num
        self.doors = doors #number
        self.seats = seats #number
        self.horsepower = horsepower #number
        self.torque = torque #number
        self.misc = misc #text
        self.sales_rep_id = sales_rep_id #text
        self.date_added = datetime.utcnow().timestamp() #float
        self.id = id

    @staticmethod
    def add_car(car):
        db.create_car(car)

    def __str__(self) -> str:
        return f"<Id: {self.id}, Descripton: {self.description}, O.E.M: {self.oem}, Model: {self.model}, : {self.model}, Year: {self.year}, Mileage: {self.mileage}, Color: {self.color}, Price: {self.price}, Drivetrain: {self.drivetrain}, Engine Cylinder: {self.engine_cylinder}, Engine Size: {self.engine_size}, Four Wheel Steering: {self.four_wheel_steering}, ABS: {self.abs}, TCS: {self.tcs}, Doors: {self.doors}, Seats: {self.seats}, Horsepower: {self.horsepower}, Torque: {self.torque}, Misc: {self.misc}, Sales Rep Id: {self.sales_rep_id}, Date Created: {datetime.fromtimestamp(self.date_added)}>"

    def __repr__(self) -> str:
        return self.__str__()