from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from db_dealer import ItemDealer


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self, name):
        item = ItemDealer.find_by_name(name)
        if item:
            return {"item": {"name": item["name"], "price": item["price"]}}
        else:
            return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        item = ItemDealer.find_by_name(name)
        if item:
            return {"message": f"An item with that name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        try:
            ItemDealer.insert(item["name"], item["price"])
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item, 201

    @jwt_required()
    def delete(self, name):
        try:
            ItemDealer.delete_item(name)
            return {"message": "Item deleted"}
        except:
            return {"message": "Item not found"}, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemDealer.find_by_name(name)
        if item:
            try:
                ItemDealer.update(name, data["price"])
            except:
                return {"message": "An error occurred updating the item."}, 500
            return {"message": "Item has been updated"}, 200
        else:
            try:
                ItemDealer.insert(name, data["price"])
            except:
                return {"message": "An error occurred inserting the item."}, 500
            return {"message": "Item created successfully."}, 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemDealer.select_all_items()
        if items["items"]:
            return items
        else:
            return {"message": "There aren't any items stored in db."}
