import os
import sqlite3
from database import DatabaseDriver
from models import User, SalesRep, Favorite, Car, Image, Message, DirectMessage
import threading
import time
from database import db as raw_db

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
                engine_cylinder TEXT,
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

    # usage create_user(user)
    def create_user(self, user):
        self.conn.execute("""
            INSERT INTO users (username, email, timestamp_date_joined, password_hash, super_user)
            VALUES (?,?,?,?,?);
        """,
            (user.username, user.email, user.date_joined, user.password_hash, user.super_user)
        )
        self.conn.commit()
        threading.Thread(target=raw_db.create_user, args=([user])).start()

    # usage get_all_users()
    def get_all_users(self):
        cursor = self.conn.execute(
            """
            SELECT * FROM users;
            """
        )
        users = [row for row in cursor]
        return users
    
    # TODO IF DOESNT EXIST THEN REFRESH THE DATABASE AND THEN IF STILL DOESNT EXIST RETURN NULL
    # FOR Messages just have it be a post request and not even be apart of app.py
    # usage get_user_by_id((id,))
    # returns [] if no user with id exists
    def get_user_by_id(self, values):
        cursor = self.conn.execute(
        """
            SELECT * FROM users WHERE id=?;
        """,
            (str(int(values[0])),)
        )
        return [row for row in cursor]
    
    # usage get_user_by_username((username,))
    def get_user_by_username(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM users
                WHERE username=?;
            """,
            values
        )
        return [row for row in cursor]
    
    # usage create_car(car)
    def create_car(self, car):
        self.conn.execute(
            """
                INSERT INTO cars (sales_rep_id, description, oem, model, year, mileage, color, 
                            price, drivetrain, engine_cylinder, engine_size, four_wheel_steering, 
                            abs, tcs, doors, seats, horsepower, torque, misc, date_added)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (car.sales_rep_id, car.description, car.oem, car.model, car.year, car.mileage, 
              car.color, car.price, car.drivetrain, car.engine_cylinder, car.engine_size, 
              car.four_wheel_steering, car.abs, car.tcs, car.doors, car.seats, car.horsepower, 
              car.torque, car.misc, car.date_added)
        )
        self.conn.commit()
        threading.Thread(target=raw_db.create_car, args=((car,))).start()

    # usage get_all_cars()
    def get_all_cars(self):
        cursor = self.conn.execute(
            """
                SELECT * FROM cars
                WHERE id > 12;
            """
        )
        return [row for row in cursor]

    # not used in production
    def testing_get_all_cars(self):
        cursor = self.conn.execute(
            """
                SELECT * FROM cars;
            """
        )
        return [row for row in cursor]

    # usage get_car_by_id(id)
    def get_car_by_id(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM cars
                WHERE id=?;
            """,
            (values,)
        )
        out = [row for row in cursor]    
        return out
    
    # usage create_image((image.link, image.car_id, image.cover_img))
    def create_image(self, values):
        self.conn.execute(
            """
                INSERT INTO images (link, car_id, cover_img)
                VALUES (?,?,?);
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.create_image, args=((values,))).start()

    # usage get_images_from_car_id(id)
    def get_images_from_car_id(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM images
                WHERE car_id=?;
            """,
            (values,)
        )
        return [row for row in cursor]
    
    # usage paginate_cars((cars_per_page, index))
    def paginate_cars(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM cars
                LIMIT ?
                OFFSET ?;
            """,
            values
        )
        return [row for row in cursor]
        
    # usage create_sales_rep((id,about,image_link))
    def create_sales_rep(self, values):
        self.conn.execute(
            """
                INSERT INTO sales_reps (user_id, about, image_link)
                VALUES (?, ?, ?);
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.create_sales_rep, args=((values,))).start()

    # usage update_sales_rep_about((about, user_id))
    def update_sales_rep_about(self, values):
        self.conn.execute(
            """
                UPDATE sales_reps
                SET about=? 
                WHERE user_id=?;
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.update_sales_rep_about, args=((values,))).start()

    # usage update_sales_rep_image_link((link, user_id))
    def update_sales_rep_image_link(self, values):
        self.conn.execute(
            """
                UPDATE sales_reps
                SET image_link=?
                WHERE user_id=?;
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.update_sales_rep_image_link, args=((values,))).start()

    # usage get_sales_rep_by_user_id((id))
    def get_sales_rep_by_user_id(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM sales_reps 
                WHERE user_id=? 
                LIMIT 1; 
            """,
            (values,)
        )
        return [row for row in cursor]

    # usage get_all_sales_reps()
    def get_all_sales_reps(self):
        cursor = self.conn.execute(
            """
                SELECT * FROM sales_reps;
            """
        )
        return [row for row in cursor]
    
    # usage create_message((name, message))
    def create_message(self, values):
        self.conn.execute(
            """
                INSERT INTO messages (name, message)
                VALUES (?,?);
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.create_message, args=((values,))).start()

    # usage get_cars_by_sales_rep_id((id))
    def get_cars_by_sales_rep_id(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM cars
                WHERE sales_rep_id=?;
            """,
            (values,)
        )
        return [row for row in cursor]
    
    # usage get_sales_rep_by_user_id((id))
    def get_sales_rep_by_user_id(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM sales_reps
                WHERE user_id=?;
            """,
            (values,)
        )
        return [row for row in cursor]
    
    # usage assign_sales_rep((user_id, car_id))
    def assign_sales_rep(self, values):
        self.conn.execute(
            """
                UPDATE cars
                SET sales_rep_id=?
                WHERE id=?;
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.assign_sales_rep, args=((values,))).start()

    # usage add_favorite((user_id, car_id))
    def add_favorite(self, values):
        self.conn.execute(
            """
                INSERT INTO favorites (user_id, car_id)
                VALUES (?,?);
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.add_favorite, args=((values,))).start()

    # usage remove_favorite((user_id, car_id))
    def remove_favorite(self, values):
        self.conn.execute(
            """
                DELETE FROM favorites
                WHERE user_id=? AND car_id=?;
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.remove_favorite, args=((values,))).start()

    # usage is_car_favorited((user_id, car_id))
    def is_car_favorited(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM favorites
                WHERE user_id=? AND car_id=?;
            """,
            values
        )
        return [row for row in cursor]
    
    # usage get_all_favorited((user_id))
    def get_all_favorited(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM cars
                JOIN favorites
                ON cars.id=favorites.car_id
                WHERE user_id=?;
            """,
            (values,)
        )
        output = [row for row in cursor]
        if not len(output) > 0:
            return []
        return [v[0:21] for v in output]
    
    # usage send_direct_message((sender_id, recipient_id, content, datetime.utcnow().timestamp()))
    def send_direct_message(self, values):
        self.conn.execute(
            """
                INSERT INTO direct_messages (sender_id, recipient_id, content, time_sent)
                VALUES (?,?,?,?);          
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.send_direct_message, args=((values,))).start()

    # usage get_messages((sender_id, recipient_id))
    def get_messages(self, values):
        cursor = self.conn.execute(
            """
                SELECT * FROM direct_messages
                WHERE sender_id=? AND recipient_id=?;
            """,
            values
        )
        return [row for row in cursor]
    
    # usage NOT USED BY MODELS
    def get_all_cars_with_images(self):
        pass

    # usage direct_message_senders((user_id))
    def direct_message_senders(self, values):
        cursor = self.conn.execute(
            """
                SELECT sender_id FROM direct_messages 
                WHERE recipient_id=?
                GROUP BY sender_id;
            """,
            (values,)
        )
        return [row for row in cursor]
    
    # usage change_password((password_hash, id))
    def change_password(self, values):
        self.conn.execute(
            """
                UPDATE users 
                SET password_hash=? 
                WHERE id=?;
            """,
            values
        )
        self.conn.commit()
        threading.Thread(target=raw_db.change_password, args=((values,))).start()

    def add_favorite_thread_test(self):
        threading.Thread(target=raw_db.add_favorite, args=((69,69),)).start()
        
    def thread(self):
        def threaded_function():
            print("thread starting")
            time.sleep(10)
            print("thread finished")
        print("before thread activate")
        threading.Thread(target=threaded_function).start()
        print("after thread activate")

cache_db = Cache()