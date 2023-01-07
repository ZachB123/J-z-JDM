import pymysql
from config import Config

class DatabaseDriver():

    def db_op(self, sql, values=()):
        connection = pymysql.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER, password=Config.DATABASE_PASSWORD, port=int(Config.DATABASE_PORT), db=Config.DATABASE)
        output = None
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

    # def create_cars_table(self):
    #     self.db_op("""
        
    #     """, ())

    # def create_sales_reps_table(self):
    #     self.db_op("""
    #         CREATE TABLE sales_reps(
    #             id int NOT NULL,
    #             user_id int NOT NULL,
    #             about TEXT,
    #             PRIMARY KEY (id),
    #             FOREIGN KEY (user_id) REFERENCES users(id)
    #         );
    #     """, ())

# FOREIGN KEY (user_id) REFERENCES users(id)
db = DatabaseDriver()
# db.create_sales_reps_table()
