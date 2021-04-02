from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Cart(db.Model):

    order_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.String, nullable=False)
    order_datetime = db.Column(db.DateTime, nullable=False)
    rs_quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    rs_delivered_status = db.Column(db.Boolean, nullable=False)


    def __init__(self, order_id, booking_id, item_id, order_datetime, rs_quantity, price, rs_delivered_status):
        self.order_id = order_id
        self.booking_id = booking_id
        self.item_id = item_id
        self.order_datetime = order_datetime
        self.rs_quantity = rs_quantity
        self.price = price
        self.rs_delivered_status = rs_delivered_status
        

    def json(self):
        return {"order_id": self.order_id, "booking_id": self.booking_id, 
        "item_id": self.item_id, "order_datetime": self.order_datetime, 
        "rs_quantity": self.rs_quantity, "price": self.price,
        "rs_delivered_status": self.rs_delivered_status}

# getting all room service/facility booking request by booking_id
# requires booking_id in url
@app.route("/cart/booking/<string:booking_id>")
def get_by_bookingID(booking_id):
    bookings = Cart.query.filter_by(booking_id=booking_id).all()
    if len(bookings):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bookings": [booking.json() for booking in bookings]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no room service or facility bookings."
        }
    ), 404

# getting information about a room service/facility booking request by order_id
# requires order_id in url
@app.route("/cart/order/<string:order_id>")
def get_by_orderID(order_id):
    order = Cart.query.filter_by(order_id=order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Booking not found."
        }
    ), 404

# create new facility booking 
# requires item_id in body request
@app.route("/cart/add_fb/<string:booking_id>", methods=['POST'])
def create_fb(booking_id):
    data = request.get_json()
    new_fb = Cart(order_id=None, booking_id=booking_id, order_datetime=None, rs_quantity=None, price=None, rs_delivered_status=None **data)

    try:
        db.session.add(new_fb)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the facility booking." + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_fb.json()
        }
    ), 201

# Create new room service
# requires item_id, rs_quantity and price in body request
@app.route("/cart/add_rs/<string:booking_id>", methods=['POST'])
def create_rs_order(booking_id):
    data = request.get_json()
    new_rs = Cart(order_id=None, booking_id=booking_id, order_datetime=None, rs_delivered_status=False, **data)

    try:
        db.session.add(new_rs)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "booking_id": booking_id
                },
                "message": "An error occurred creating the room service order."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_rs.json()
        }
    ), 201


# Get the number of bookings of a specific facility at a specific timeslot
# requires item_id and order_datetime in url, format of datetime is YYYY-MM-DD HH for filtering by hourly
@app.route("/cart/item_id=<string:item_id>&order_datetime=<string:order_datetime>")
def get_number_of_bookings(item_id,order_datetime):
    total = Cart.query.filter((Cart.order_datetime.like(order_datetime + "%")) & (Cart.item_id==item_id)).all()
    if len(total) >= 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    # "bookings": [booking.json() for booking in total], #can remove if we just need the total number
                    "total": len(total)
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Error."
        }
    ), 404

# Get all room service by booking_id
# requires booking_id in url
@app.route("/cart/room_service/<string:booking_id>")
def get_all_room_service(booking_id):
    all_room_service = Cart.query.filter((Cart.item_id.like("rs%")) & (Cart.booking_id==booking_id)).all()
    if len(all_room_service):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "all_room_service": [room_service.json() for room_service in all_room_service]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no room service orders."
        }
    ), 404

# update specific room service status to TRUE
# requires order_id in URL and "rs_delivered_status": true in body
@app.route("/cart/room_service/<string:order_id>", methods=['PUT'])
def update_room_service(order_id):
    try:
        room_service = Cart.query.filter_by(order_id=order_id).first()
        if not room_service:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "order_id": order_id
                    },
                    "message": "Room service order not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['rs_delivered_status']:
            room_service.rs_delivered_status = data['rs_delivered_status']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": room_service.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": order_id
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)



