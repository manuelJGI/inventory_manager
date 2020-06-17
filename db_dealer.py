import sqlite3
import sys


class DBSource:
    def __enter__(self):
        self.connection = sqlite3.connect("data.db")
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.connection.commit()
        else:
            print("error: ", file=sys.stderr)
            self.connection.rollback()

        self.connection.close()


class UserDealer:
    @classmethod
    def find_by_column(cls, datum, column):
        with DBSource() as dbdealer:
            query = f"SELECT * FROM users WHERE {column}=?"
            result = dbdealer.execute(query, (datum,))
            row = result.fetchone()
            if row:
                return dict(_id=row[0], username=row[1], password=row[2])
            return None

    @classmethod
    def register_user(cls, username, password):
        with DBSource() as source:
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            source.execute(query, (username, password))
