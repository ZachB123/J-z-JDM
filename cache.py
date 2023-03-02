import os
import sqlite3
from database import DatabaseDriver
from models import User, SalesRep, Favorite, Car, Image, Message, DirectMessage

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance

class Cache():

    TABLE_NAMES = ["cars", "direct_messages", "favorites", "images", "messages", "sales_reps", "users"]

    def __init__(self):
        self.remove_cache_db()
        self.conn = sqlite3.connect("cache.db", check_same_thread=False)
        self.data = self.get_data()
        self.create_tables()
        self.add_data()

    def does_cache_exist(self):
        current_directory = os.getcwd()
        cache_db_path = os.path.join(current_directory, "cache.db")
        if os.path.exists(cache_db_path):
            return True
        return False
    
    def remove_cache_db(self):
        current_directory = os.getcwd()
        cache_db_path = os.path.join(current_directory, "cache.db")
        if os.path.exists(cache_db_path):
            os.remove(cache_db_path)

    def get_data(self):
        database = DatabaseDriver()
        return database.get_all(self.TABLE_NAMES)
    
    def add_data(self):
        self.add_cars()
        self.add_direct_messages()
        self.add_favorites()
        self.add_images()
        self.add_messages()
        self.add_sales_reps()
        self.add_users()

    def add_cars(self):
        cars = self.data["cars"]
        for car in [Car.car_from_tuple(t) for t in cars]:
            self.add_car_to_db(car)
        print("cars added")

    def add_car_to_db(self, car):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO cars (id, sales_rep_id, description, oem, model, year, mileage, color, price, drivetrain, engine_cylinder, engine_size, four_wheel_steering, abs, tcs, doors, seats, horsepower, torque, misc, date_added)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
            """,
            (car.id, car.sales_rep_id, car.description, car.oem, car.model, car.year, car.mileage, car.color, car.price, car.drivetrain, car.engine_cylinder, car.engine_size, car.four_wheel_steering, car.abs, car.tcs, car.doors, car.seats, car.horsepower, car.torque, car.misc, car.date_added)
        )
        self.conn.commit()

    def add_direct_messages(self):
        direct_messages = self.data["direct_messages"]
        for message in [DirectMessage.direct_message_from_tuple(t) for t in direct_messages]:
            self.add_direct_message_to_db(message)
        print("direct_messages added")

    def add_direct_message_to_db(self, message):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO direct_messages (id, sender_id, recipient_id, content, time_sent, is_read)
            VALUES (?,?,?,?,?,?);
            """,
            (message.id, message.sender_id, message.recipient_id, message.message, message.timestamp, message.is_read)
        )
        self.conn.commit()

    def add_favorites(self):
        favorites = self.data["favorites"]
        for favorite in Favorite.create_favorite_list_from_list(list(favorites)):
            self.add_favorite_to_db(favorite)
        print("favorites added")

    def add_favorite_to_db(self, favorite):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO favorites (id, user_id, car_id)
            VALUES(?,?,?);
            """,
            (favorite.id, favorite.user_id, favorite.car_id)
        )
        self.conn.commit()

    def add_images(self):
        images = self.data["images"]
        for image in Image.images_from_list(list(images)):
            self.add_image_to_db(image)
        print("images added")

    def add_image_to_db(self, image):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO images (id, link, car_id, cover_img)
            VALUES (?,?,?,?);
            """,
            (image.id, image.link, image.car_id, image.cover_img)
        )
        self.conn.commit()

    def add_messages(self):
        messages = self.data["messages"]
        for message in [Message.message_from_tuple(t) for t in messages]:
            self.add_message_to_db(message)
        print("messages added")

    def add_message_to_db(self, message):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO messages (id, name, message)
            VALUES (?,?,?);
            """,
            (message.id, message.name, message.message)
        )
        self.conn.commit()

    def add_sales_reps(self):
        sales_reps = self.data["sales_reps"]
        for sales_rep in [SalesRep.sales_rep_from_tuple(t) for t in sales_reps]:
            self.add_sales_rep_to_db(sales_rep)
        print("sales reps added")

    def add_sales_rep_to_db(self, sales_rep):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO sales_reps (id, user_id, about, image_link)
            VALUES (?,?,?,?);
            """,
            (sales_rep.id, sales_rep.user.id, sales_rep.about, sales_rep.image_link)
        )
        self.conn.commit()

    def add_users(self):
        users = User.users_from_list(list(self.data["users"]))
        for user in users:
            self.add_user_to_db(user)
        print("users added")

    def add_user_to_db(self, user):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (id, username, email, timestamp_date_joined, password_hash, super_user)
            VALUES (?,?,?,?,?,?);
            """,
            (user.id, user.username, user.email, user.date_joined, user.password_hash, user.super_user)
        )
        self.conn.commit()

    def create_tables(self):
        self.create_cars_table()
        self.create_direct_messages_table()
        self.create_favorites_table()
        self.create_images_table()
        self.create_messages_table()
        self.create_sales_rep_table()
        self.create_users_table()


    def create_cars_table(self):
        sql = """
            CREATE TABLE cars (
                id INTEGER,
                sales_rep_id INTEGER,
                description TEXT,
                oem TEXT,
                model TEXT,
                year INTEGER,
                mileage INTEGER,
                color TEXT,
                price INTEGER,
                drivetrain TEXT,
                engine_cylinder INTEGER,
                engine_size INTEGER,
                four_wheel_steering INTEGER,
                abs INTEGER,
                tcs INTEGER,
                doors INTEGER,
                seats INTEGER,
                horsepower INTEGER,
                torque INTEGER,
                misc TEXT,
                date_added REAL
            );
        """
        self.create_table(sql) 

    def create_direct_messages_table(self):
        sql = """
            CREATE TABLE direct_messages (
                id INTEGER,    
                sender_id INTEGER,       
                recipient_id INTEGER,
                content TEXT,
                time_sent INTEGER,
                is_read INTEGER
            );
        """
        self.create_table(sql)

    def create_favorites_table(self):
        sql = """
            CREATE TABLE favorites (
                id INTEGER,
                user_id INTEGER,
                car_id INTEGER
            );
        """
        self.create_table(sql)

    def create_images_table(self):
        sql = """
            CREATE TABLE images (
                id INTEGER,
                link TEXT,
                car_id INTEGER,
                cover_img INTEGER
            );
        """
        self.create_table(sql) 

    def create_messages_table(self):
        sql = """
            CREATE TABLE messages (
                id INTEGER,
                name TEXT,
                message TEXT
            );
        """
        self.create_table(sql)  

    def create_sales_rep_table(self):
        sql = """
            CREATE TABLE sales_reps (
                id INTEGER,
                user_id INTEGER,
                about TEXT,
                image_link TEXT
            );
        """
        self.create_table(sql)   

    def create_users_table(self):
        sql = """
            CREATE TABLE users (
                id INTEGER,
                username TEXT,
                email TEXT,
                timestamp_date_joined REAL,
                password_hash TEXT,
                super_user INTEGER
            );
        """
        self.create_table(sql)   

    def create_table(self, sql):
        try:
            self.conn.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)

    def get_all_users(self):
        cursor = self.conn.execute(
            """
            SELECT * FROM users;
            """
        )
        users = [row for row in cursor]
        return users
    
    def get_user_by_id(self, values):
        sql = f"SELECT * FROM users WHERE id={values[0]};"
        cursor = self.conn.execute(sql)
        return [row for row in cursor]
        




cache_db = Cache()