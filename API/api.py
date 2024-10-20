from flask import Flask, request, jsonify, session
from service import ToDoService
from flask_cors import CORS
from models import Schema, UserModel
import json
import logging


app = Flask(__name__)
app.secret_key = 'super_secret_key_that_will_never_be_cracked'

CORS(app)

@app.after_request
def add_headers(response):
   response.headers['Access-Control-Allow-Origin'] = "*"
   response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
   response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
   return response


@app.route("/todo", methods=["GET"])
def list_todo():
   params = request.args
   username = params.get('Username')
   password = params.get('Password')

   if not username or not password:
      return jsonify({"error": "Missing username or password"}), 400

   user_model = UserModel()
   user = user_model.get_by_username(username)

   if user and user['Password'] == password:
      # Fetch and return todos associated with the user's ID
      todos = ToDoService().list_by_user_id(user['Id'])  # Use user ID instead of username
      return jsonify(todos), 200
   else:
      return jsonify({"error": "Invalid username or password"}), 401


@app.route("/todo", methods=["POST"])
def create_todo():
    params = request.get_json()
    username = params.get('Username')
    password = params.get('Password')
    
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user_model = UserModel()
    user = user_model.get_by_username(username)

    if user and user['Password'] == password:
        # Retrieve todo data from the request payload
        todo_data = {
            'Title': params.get('Title'),
            'Description': params.get('Description'),
            'DueDate': params.get('DueDate'),
            'UserId': user['Id'] 
        }

        # Check if all required fields are present
        if not todo_data['Title'] or not todo_data['Description'] or not todo_data['DueDate']:
            return jsonify({"error": "Missing todo data"}), 400

        # Create the todo item
        return jsonify(ToDoService().create(todo_data)), 201
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route("/todo/<item_id>", methods=["PUT"])
def update_item(item_id):
   params = request.args
   username = params.get('Username')
   password = params.get('Password')

   if not username or not password:
      return jsonify({"error": "Missing username or password"}), 400

   # Fetch the user from the database
   user_model = UserModel()
   user = user_model.get_by_username(username)

   if not user or user['Password'] != password:
      return jsonify({"error": "Invalid username or password"}), 401

   todo = ToDoService().get_by_id(item_id)
   if todo:
      todo_dict = {
         'Id': todo[0],
         'Title': todo[1],
         'Description': todo[2],
         'DueDate': todo[3],
         'UserId': todo[4]  # Adjust based on your tuple structure
      }

      if todo_dict['UserId'] != user['Id']:
         return jsonify({"error": "Unauthorized"}), 401

   else:
      return jsonify({"error": "Todo item not found"}), 404

   # Update todo logic here
   updated_data = request.get_json()
   # Assuming you have a function to update the todo
   ToDoService().update(item_id, updated_data)
   return jsonify({"message": "Todo updated successfully"}), 200

@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
   params = request.args
   username = params.get('Username')
   password = params.get('Password')

   if not username or not password:
      return jsonify({"error": "Missing username or password"}), 400

   user_model = UserModel()
   user = user_model.get_by_username(username)

   if not user or user['Password'] != password:
      return jsonify({"error": "Invalid username or password"}), 401

   todo = ToDoService().get_by_id(item_id)
   if todo:
      todo_dict = {
         'Id': todo[0],
         'Title': todo[1],
         'Description': todo[2],
         'DueDate': todo[3],
         'UserId': todo[4]  # Adjust based on your tuple structure
      }

      if todo_dict['UserId'] != user['Id']:
         return jsonify({"error": "Unauthorized"}), 401

      ToDoService().delete(item_id)
      return jsonify({"message": "Todo deleted successfully"}), 200
   else:
      return jsonify({"error": "Todo item not found"}), 404

@app.route("/todo/<item_id>", methods=["GET"])
def get_item(item_id):
   params = request.args
   username = params.get('Username')
   password = params.get('Password')

   if not username or not password:
      return jsonify({"error": "Missing username or password"}), 400

   user_model = UserModel()
   user = user_model.get_by_username(username)

   if not user or user['Password'] != password:
      return jsonify({"error": "Invalid username or password"}), 401

   todo = ToDoService().get_by_id(item_id)
   if todo:
      todo_dict = {
         'Id': todo[0],
         'Title': todo[1],
         'Description': todo[2],
         'DueDate': todo[3],
         'UserId': todo[4]  # Adjust based on your tuple structure
      }

      if todo_dict['UserId'] != user['Id']:
         return jsonify({"error": "Unauthorized"}), 401

      return jsonify(todo_dict), 200
   else:
      return jsonify({"error": "Todo item not found"}), 404


@app.route("/login", methods=["POST"])
def login_user():
   params = request.get_json()
   if 'Username' not in params or 'Password' not in params:
      return jsonify({"error": "Missing username or password"}), 400
   
   user_model = UserModel()
   
   user = user_model.get_by_username(params['Username'])

   if user:
      if user['Password'] == params['Password']:
         session['user_id'] = user['Id']
         return jsonify(user)
      else:
         return jsonify({"error": "Invalid username or password"}), 401
   else:
      new_user = user_model.create(params)
      if new_user:
         session['user_id'] = new_user['Id']
         return jsonify(new_user), 201
      else:
         print("Failed to create new user.")  # Log failure to create user
         return jsonify({"error": "Failed to create user"}), 500

if __name__ == "__main__":
   Schema()
   app.run(host="0.0.0.0", port=5000)
