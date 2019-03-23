import sqlite3

from werkzeug.security import generate_password_hash

from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username, ))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id, ))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    def post(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        req = reqparse.RequestParser()
        req.add_argument('username', type=str, required=True,
                         help="username is required")
        req.add_argument('password', type=str, required=True,
                         help="password is required")
        data = req.parse_args()
        hashed_password = generate_password_hash(data['password'])
        if User.find_by_username(data['username']):
            return {"message": "user already exists"}, 400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], hashed_password))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
