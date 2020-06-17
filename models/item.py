import sqlite3
from db_dealer import DBSource


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"items": {"name": self.name, "price": self.price}}

    def update(self):
        with DBSource() as dbdealer:
            query = "UPDATE items SET price=? WHERE name=?"
            dbdealer.execute(query, (self.price, self.name))

    def insert(self):
        with DBSource() as dbdealer:
            query = "INSERT INTO items VALUES (?,?)"
            dbdealer.execute(query, (self.name, self.price))

    @classmethod
    def find_by_name(cls, name):
        with DBSource() as dbdealer:
            query = "SELECT * FROM items WHERE name=?"
            result = dbdealer.execute(query, (name,))
            row = result.fetchone()
        if row:
            return cls(*row)
        return None

    @classmethod
    def select_all_items(cls, limit=100):
        with DBSource() as dbdealer:
            query = "SELECT * FROM items LIMIT ?"
            result = dbdealer.execute(query, (limit,))
            rows = result.fetchall()
        return {"items": [dict(name=row[0], price=row[1]) for row in rows]}

    def delete_item(self):
        if self.find_by_name(self.name):
            with DBSource() as dbdealer:
                query = "DELETE FROM items WHERE name=?"
                dbdealer.execute(query, (self.name,))
        else:
            raise sqlite3.OperationalError("Item not found")
