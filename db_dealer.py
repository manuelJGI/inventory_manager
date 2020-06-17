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


class ItemDealer:
    @classmethod
    def update(cls, name, price):
        with DBSource() as dbdealer:
            query = "UPDATE items SET price=? WHERE name=?"
            dbdealer.execute(query, (price, name))

    @classmethod
    def insert(cls, name, price):
        with DBSource() as dbdealer:
            query = "INSERT INTO items VALUES (?,?)"
            dbdealer.execute(query, (name, price))

    @classmethod
    def find_by_name(cls, name):
        with DBSource() as dbdealer:
            query = "SELECT * FROM items WHERE name=?"
            result = dbdealer.execute(query, (name,))
            row = result.fetchone()

        if row:
            return {"name": row[0], "price": row[1]}
        return None

    @classmethod
    def select_all_items(cls, limit=100):
        with DBSource() as dbdealer:
            query = "SELECT * FROM items LIMIT ?"
            result = dbdealer.execute(query, (limit,))
            rows = result.fetchall()
        return {"items": [dict(name=row[0], price=row[1]) for row in rows]}

    @classmethod
    def delete_item(cls, name):
        if cls.find_by_name(name):
            with DBSource() as dbdealer:
                query = "DELETE FROM items WHERE name=?"
                dbdealer.execute(query, (name,))
        else:
            raise sqlite3.OperationalError("Item not found")


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
