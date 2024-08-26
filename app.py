from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # def __init__(self, username, email):
    #     self.username = username
    #     self.email = email

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

db.create_all()

#test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({"message": "Hello ffffff"}), 200)

#create a user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        print(new_user, data)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "User created"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Error creating user", "error": str(e), }), 500)
#get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Error getting users"}), 500)


#get user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        if user:
            return make_response(jsonify(user.json()), 200)
        else:
            return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Error getting user"}), 500)

#update user by id
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({"message": "User updated"}), 200)
        else:
            return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Error updating user"}), 500)

#delete user by id
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "User deleted"}), 200)
        else:
            return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Error deleting user"}), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)