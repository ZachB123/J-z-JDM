import pymysql
from config import Config

class DatabaseDriver():

    def db_op(self, sql, values):
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
        return self.db_op("""SELECT * FROM test;""", ())

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
        

    def drop_user_table(self):
        self.db_op("""
            DROP TABLE user;
        """, ())


db = DatabaseDriver()
