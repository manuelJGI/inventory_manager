from db_dealer import DBSource
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.FLOAT(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"items": {"name": self.name, "price": self.price}}

    def update(self):
        with DBSource() as dbdealer:
            query = "UPDATE items SET price=? WHERE name=?"
            dbdealer.execute(query, (self.price, self.name))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def select_all_items(cls, limit=100):
        with DBSource() as dbdealer:
            query = "SELECT * FROM items LIMIT ?"
            result = dbdealer.execute(query, (limit,))
            rows = result.fetchall()
        return {"items": [dict(name=row[0], price=row[1]) for row in rows]}

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
