from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/room_service'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:3306/room_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

# getting all room service information
@app.route("/room_service")
def get_all():
    room_services = Room_Service.query.all()
    if len(room_services):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "room_services": [room_service.json() for room_service in room_services]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no room services."
        }
    ), 404


# getting information about a room service by item_id
# requires item_id in url
@app.route("/room_service/<string:item_id>")
def get_by_itemID(item_id):
    rm_items = Room_Service.query.filter_by(item_id=item_id).first()
    if rm_items:
        return jsonify(
            {
                "code": 200,
                "data": rm_items.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Room Service not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5003, debug=True)
