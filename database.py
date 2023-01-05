import pymysql

class DatabaseDriver():

    def db_op(self, sql, values):
        connection = pymysql.connect(host="containers-us-west-160.railway.app", user="root", password="yloA9qnKqIfDgTSWipf7", port=7036, db="railway")
        output = None
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                output = cursor.fetchall()
            connection.commit()
        return output

    def delete_all_from_test(self):
        self.db_op("""DELETE FROM test""", ())

    def add_post(self, values):
        self.db_op("""INSERT INTO test (data, name) VALUES (%s,%s)""", values)

    def get_all_posts(self):
        return list(self.db_op("""SELECT * FROM test""", ()))


db = DatabaseDriver()