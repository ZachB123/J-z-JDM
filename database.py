import pymysql
from config import Config

class DatabaseDriver():

    def db_op(self, sql, values=()):
        output = None
        connection = pymysql.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER, password=Config.DATABASE_PASSWORD, port=int(Config.DATABASE_PORT), db=Config.DATABASE)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                output = cursor.fetchall()
            connection.commit()
        return list(output)

    def delete_all_from_test(self):
        self.db_op("""DELETE FROM test;""", ())

    def add_post(self, values):
        self.db_op("""INSERT INTO test (data, name) VALUES (%s,%s);""", values)

    def get_all_posts(self):
        return self.db_op("""SELECT * FROM test;""")

    # order is username email date_joined super_user
    # user object is passed in
    def create_user(self, user):
        self.db_op("""
            INSERT INTO users (username, email, timestamp_date_joined, password_hash, super_user)
            VALUES (%s, %s, %s, %s, %s);
        """, (user.username, user.email, user.date_joined, user.password_hash, user.super_user))

    def get_all_users(self):
        return self.db_op("""
            SELECT * FROM users;
        """)

    def get_user_by_id(self, values):
        return self.db_op("""SELECT * FROM users WHERE id=%s; """, values)

    def get_user_by_username(self, values):
        return self.db_op("""
            SELECT * FROM users
            WHERE username=%s;
        """, values)
    
    def create_car(self, car):
        self.db_op("""
            INSERT INTO cars (sales_rep_id, description, oem, model, year, mileage, color, price, drivetrain, engine_cylinder, engine_size, four_wheel_steering, abs, tcs, doors, seats, horsepower, torque, misc, date_added)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (car.sales_rep_id, car.description, car.oem, car.model, car.year, car.mileage, car.color, car.price, car.drivetrain, car.engine_cylinder, car.engine_size, car.four_wheel_steering, car.abs, car.tcs, car.doors, car.seats, car.horsepower, car.torque, car.misc, car.date_added))

    def create_car_test(self, car):
        self.db_op("""
            INSERT INTO car_test (description)
            VALUES (%s);
        """, (car.description,))

    def get_all_cars(self):
        return self.db_op("""
            SELECT * FROM cars;
        """)

    def get_car_by_id(self, values):
        return self.db_op("""
            SELECT * FROM cars WHERE id=%s;
        """, values)

    def create_image(self, values):
        self.db_op("""
            INSERT INTO images (link, car_id, cover_img)
            VALUES (%s, %s, %s);
        """, values)

    def get_images_from_car_id(self, values):
        return self.db_op("""
            SELECT * FROM images
            WHERE car_id=%s;
        """, values)

    def paginate_cars(self, values):
        return self.db_op("""
            SELECT * FROM cars
            LIMIT %s
            OFFSET %s;
        """, values)

    def create_sales_rep(self, values):
        self.db_op("""
            INSERT INTO sales_reps (user_id, about, image_link)
            VALUES (%s, %s, %s);
        """, values)

    def update_sales_rep_about(self, values):
        self.db_op("""
            UPDATE sales_reps
            SET about=%s 
            WHERE user_id=%s;
        """, values)

    def update_sales_rep_image_link(self, values):
        self.db_op("""
            UPDATE sales_reps
            SET image_link=%s 
            WHERE user_id=%s;
        """, values)

    def get_sales_rep_by_user_id(self, values):
        return self.db_op("""
            SELECT * FROM sales_reps 
            WHERE user_id=%s 
            LIMIT 1;
        """, values)

    def get_all_sales_reps(self):
        return self.db_op("""
            SELECT * FROM sales_reps;
        """)

    def create_message(self, values):
        self.db_op("""
            INSERT INTO messages (name, message)
            VALUES (%s, %s);
        """, values)

    def get_cars_by_sales_rep_id(self, values):
        return self.db_op("""
            SELECT * FROM cars
            WHERE sales_rep_id=%s;
        """, values)

    def get_sales_reps_by_user_id(self, values):
        return self.db_op("""
            SELECT * FROM sales_reps 
            WHERE user_id=%s;
        """, values)

    def assign_sales_rep(self, values):
        self.db_op("""
            UPDATE cars 
            SET sales_rep_id=%s
            WHERE id=%s;
        """, values)

    def add_favorite(self, values):
        self.db_op("""
            INSERT INTO favorites (user_id, car_id)
            VALUES (%s, %s);
        """, values)

    def remove_favorite(self, values):
        self.db_op("""
            DELETE FROM favorites 
            WHERE user_id=%s AND car_id=%s;
        """, values)

    def is_car_favorited(self, values):
        return self.db_op("""
            SELECT * FROM favorites 
            WHERE user_id=%s AND car_id=%s;
        """, values)

    def get_all_favorited(self, values):
        query = self.db_op("""
            SELECT * FROM cars
            JOIN favorites
            ON cars.id=favorites.car_id
            WHERE user_id=%s;
        """, values)
        if not len(query) > 0:
            return []
        return [v[0:21] for v in query]

    def send_direct_message(self, values):
        self.db_op("""
            INSERT INTO direct_messages (sender_id, recipient_id, content, time_sent)
            VALUES (%s, %s, %s, %s);
        """, values)

    def get_messages(self, values):
        return self.db_op("""
            SELECT * FROM direct_messages
            WHERE sender_id=%s AND recipient_id=%s;
        """, values)

    def get_all_cars_with_images(self):
        return self.db_op("""
            SELECT * FROM cars  
            JOIN images 
            ON cars.id=images.car_id;
        """)
        


db = DatabaseDriver()
