from flask import Flask, jsonify

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'my item',
                'price': 15.99
            }
        ]
    }
]


@app.route('/store', methods=['POST'])
def create_store():
    pass


@app.route('/store')
def get_store():
    pass


@app.route('/store/<string:name>')
def get_stores(name):
    return jsonify({'stores': stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store():
    pass


@app.route('/store/<string:name>')
def get_items_in_store(name):
    pass


app.run(port=3000)
