from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": f"An item with that name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        """
        simple delete endpoint for item model
        :param name: the name of the item to be deleted
        :return: json
        """
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
            return {"message": "Item deleted"}
        return {"message": "Item not found"}, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.price = data["price"]
                item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
            return {"message": "Item has been updated"}, 200
        else:
            try:
                item = ItemModel(name, data["price"])
                item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
            return {"message": "Item created successfully."}, 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.select_all_items()
        if items["items"]:
            return items
        else:
            return {"message": "There aren't any items stored in db."}
