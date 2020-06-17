from flask_restful import Resource, reqparse
from db_dealer import UserDealer


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("password", type=str, required=True, help="This field cannot be left blank")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserDealer.find_by_column(data["username"], "username"):
            return {"message": "User already exists"}, 400
        try:
            UserDealer.register_user(data["username"], data["password"])
        except:
            return {"message": "Internal server error"}, 500
        return {"message": "User created successfully"}, 201
