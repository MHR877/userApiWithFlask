from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

path = "./db/users.json"

@app.route("/test", methods=["GET"])
def test():
    return make_response(jsonify({"message": "test route"}), 200)


@app.route("/users", methods=["GET"])
def get_users():
    try:
        with open(path, "r") as users_file:
            users_data = json.load(users_file)

        return users_data
    except:
        return make_response(jsonify({"message": "error get users"}), 500)


@app.route("/users/id/<int:id>", methods=["GET"])
def get_user_by_id(id):
    try:
        with open(path, "r") as users_file:
            users_data = json.load(users_file)

        for user in users_data["users"]:
            if user["id"] == id:
                return make_response(jsonify({"message": "success", "user": user}), 200)

        return make_response(jsonify({"message": "error user not found"}), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "error retrieving user", "error": str(e)}), 500
        )


@app.route("/users/email/<email>", methods=["GET"])
def get_user_by_email(email):
    try:
        with open(path, "r") as users_file:
            users_data = json.load(users_file)

        for user in users_data["users"]:
            if user["email"] == email:
                return make_response(jsonify({"message": "success", "user": user}), 200)

        return make_response(jsonify({"message": "error user not found"}), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "error retrieving user", "error": str(e)}), 500
        )


@app.route("/users/username/<username>", methods=["GET"])
def get_user_by_username(username):
    try:
        with open(path, "r") as users_file:
            users_data = json.load(users_file)

        for user in users_data["users"]:
            if user["username"] == username:
                return make_response(jsonify({"message": "success", "user": user}), 200)

        return make_response(jsonify({"message": "error user not found"}), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "error retrieving user", "error": str(e)}), 500
        )


@app.route("/login", methods=["POST"])
def login():
    try:
        with open(path, "r") as users_file:
            users_data = json.load(users_file)

        user = request.get_json()

        for usr in list(users_data["users"]):
            if(usr["username"] == user["username"] and usr["email"] == user["email"]):
                return make_response(
                    jsonify({"message": "user login successfully", "user": usr}), 200
                )

        return make_response(
            jsonify({"message": "Email or username not correct"}), 400
        )
    except Exception as e:
        return make_response(
            jsonify({"message": "error creating user", "error": str(e)}), 500
        )


@app.route("/register", methods=["POST"])
def create_user():
    try:
        with open(path, "r") as users_file:
            users_data = json.load(users_file)
            id = len(users_data["users"]) + 1

        user = request.get_json()
        user["id"] = id

        users_data["users"].append(user)
        users_data["size"] = id

        with open(path, "w") as users_file:
            json.dump(users_data, users_file, indent=4)

        return make_response(
            jsonify({"message": "user added successfully", "user": user}), 201
        )

    except Exception as e:
        return make_response(
            jsonify({"message": "error creating user", "error": str(e)}), 500
        )


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        with open(path, "r") as users_file:
            users_data = json.load(users_file)

        res = list(filter(lambda usr: usr["id"] != int(id), users_data["users"]))
        print(res)

        users_data["users"] = res
        users_data["size"] = users_data["size"] - 1

        with open(path, "w") as users_file:
            json.dump(users_data, users_file, indent=4)

        return make_response(jsonify({"message": "user deleted successfully"}), 200)

    except Exception as e:
        return make_response(
            jsonify({"message": "error creating user", "error": str(e)}), 500
        )


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    try:
        with open(path, "r") as users_file:
            users_data = json.load(users_file)

        user = {}
        for usr in list(users_data["users"]):
            if usr["id"] == int(id):

                index = list(users_data["users"]).index(usr)
                data = request.get_json()

                for d in data:
                    usr[d] = data[d]

                user = usr
                users_data["users"][index] = usr

        with open(path, "w") as users_file:
            json.dump(users_data, users_file, indent=4)

        return make_response(
            jsonify({"message": "user updated successfully", "user": user}), 201
        )

    except Exception as e:
        return make_response(
            jsonify({"message": "error creating user", "error": str(e)}), 500
        )
