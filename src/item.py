import sqlite3

from flask_jwt import JWT, jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item does not exist'}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {
                "message": "an item with name {} already exists".format(name)
            }, 400
        req = reqparse.RequestParser()
        req.add_argument(
            'price', type=float, required=True, help="need a price field")
        data = req.parse_args()

        item = {'name': name, 'price': data['price']}

        try:

            self.insert(item)
        except:
            return {'message': 'an error occured inserting the item'}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name, ))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help="This field cannot be left blank!")
        data = parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "an error occured while inserting"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "an error occured while updating"}, 500
        return item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        res = cursor.execute(query, (item['price'], item['name']))

        items = []
        for row in res:
            items.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()

        return {'items', items}
