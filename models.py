from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from database import db
from flask_login import UserMixin
from config import Config

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

    @staticmethod
    def get_all_users():
        u = db.get_all_users()
        if len(u) > 0:
            return [User.user_from_tuple(l) for l in u]
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

class SalesRep():
    def __init__(self, user, about=None, image_link=None, id=-1):
        self.user = user
        self.about = about
        self.image_link = image_link
        self.id = id

    @staticmethod
    def add_sales_rep(sales_rep):
        db.create_sales_rep((sales_rep.user.id, sales_rep.about, sales_rep.image_link))

    @staticmethod
    def get_sales_rep_by_user_id(user_id):
        s = db.get_sales_rep_by_user_id((user_id))
        if len(s) > 0:
            return SalesRep.sales_rep_from_tuple(s[0])
        return None

    @staticmethod
    def update_sales_rep_about(sales_rep, about):
        db.update_sales_rep_about((about, sales_rep.user.id))

    @staticmethod
    def update_sales_rep_image_link(sales_rep, image_link):
        db.update_sales_rep_image_link((image_link, sales_rep.user.id))

    @staticmethod
    def sales_rep_from_tuple(t):
        return SalesRep(User.get_by_id(t[1]), t[2], t[3], t[0])

    @staticmethod
    def get_all_sales_reps():
        s = db.get_all_sales_reps()
        if len(s) > 0:
            return [SalesRep.sales_rep_from_tuple(t) for t in s]
        return None

    def __str__(self):
        return f"<Id: {self.user.id}, Username: {self.user.username}, About: {self.about}, Link: {self.image_link}>"

    def __repr__(self):
        return self.__str__()

class Car():
    def __init__(self, description, oem, model, year, mileage, color, price, drivetrain, engine_cylinder, engine_size, four_wheel_steering, abs, tcs, doors, seats, horsepower, torque, misc, sales_rep_id=-1, id=-1, date_added=-1):
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
        if date_added == -1:
            self.date_added = datetime.utcnow().timestamp() #float
        else:
            self.date_added = date_added
        self.id = id

    #returns a list of Image objects for the image for the images
    def get_images(self):
        return Image.images_from_list(db.get_images_from_car_id(self.id))

    #returns the first cover image if none returns the first result from images list
    def get_cover_image(self):
        images = Image.images_from_list(db.get_images_from_car_id(self.id))
        if not images:
            return None
        for image in images:
            if image.cover_img == 1:
                return image
        return images[0]

    @staticmethod
    def add_car(car):
        db.create_car(car)

    @staticmethod
    def get_all_cars():
        q = db.get_all_cars()
        return [Car.car_from_tuple(c) for c in q]
    
    @staticmethod
    def get_car_by_id(id):
        c = db.get_car_by_id(id)
        if len(c) > 0:
            return Car.car_from_tuple(db.get_car_by_id(id)[0])
        return None

    @staticmethod
    def car_from_tuple(c):
        return Car(c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11], c[12], c[13], c[14], c[15], c[16], c[17], c[18], c[19], c[1], c[0], c[20])

    @staticmethod
    def paginate_cars(page):
        #includes start
        return [Car.car_from_tuple(c) for c in db.paginate_cars((Config.CARS_PER_PAGE, (page-1)*Config.CARS_PER_PAGE))]

    @staticmethod
    def get_cars_by_sales_rep_id(sales_rep_id):
        return [Car.car_from_tuple(c) for c in db.get_cars_by_sales_rep_id((sales_rep_id))]
        
    def __str__(self) -> str:
        return f"<Id: {self.id}, Descripton: {self.description}, O.E.M: {self.oem}, Model: {self.model}, : {self.model}, Year: {self.year}, Mileage: {self.mileage}, Color: {self.color}, Price: {self.price}, Drivetrain: {self.drivetrain}, Engine Cylinder: {self.engine_cylinder}, Engine Size: {self.engine_size}, Four Wheel Steering: {self.four_wheel_steering}, ABS: {self.abs}, TCS: {self.tcs}, Doors: {self.doors}, Seats: {self.seats}, Horsepower: {self.horsepower}, Torque: {self.torque}, Misc: {self.misc}, Sales Rep Id: {self.sales_rep_id}, Date Created: {datetime.fromtimestamp(self.date_added)}>"

    def __repr__(self) -> str:
        return self.__str__()

class Image():
    def __init__(self, link, car_id, cover_img=0, id=-1):
        self.link = link
        self.car_id = car_id
        self.cover_img = cover_img
        self.id = id

    @staticmethod
    def add_image(image):
        db.create_image((image.link, image.car_id, image.cover_img))

    @staticmethod
    def image_from_tuple(i):
        return Image(i[1], i[2], i[3], i[0])

    @staticmethod
    def images_from_list(l):
        if len(l) > 0:
            return [Image.image_from_tuple(c) for c in l]
        return None

    def __str__(self):
        return f"<Id: {self.id}, Link: {self.link}, Car Id: {self.car_id}, Cover Image: {self.cover_img}>"

    def __repr__(self):
        return self.__str__()

class Message():
    def __init__(self, message, name=None):
        self.name = name
        self.message = message 

    @staticmethod
    def add_message(message):
        db.create_message((message.name, message.message))

