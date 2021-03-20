from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/cart'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Cart(db.Model):
    __tablename__ = 'Cart'

    order_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.String, nullable=False)
    order_datetime = db.Column(db.DateTime, nullable=False)
    rs_quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)


    def __init__(self, order_id, booking_id, item_id, order_datetime, rs_quantity, price):
        self.order_id = order_id
        self.booking_id = booking_id
        self.item_id = item_id
        self.order_datetime = order_datetime
        self.rs_quantity = rs_quantity
        self.price = price
        

    def json(self):
        return {"order_id": self.order_id, "booking_id": self.booking_id, "item_id": self.item_id, "order_datetime": self.order_datetime, "rs_quantity": self.rs_quantity, "price": self.price}

#getting all room service/facility booking request by booking_id
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
            "message": "There are no bookings."
        }
    ), 404

#getting information about a room service/facility booking request by order_id
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

#create new facility booking 
@app.route("/cart/add_fb/<string:booking_id>", methods=['POST'])
def create_fb(booking_id):
    data = request.get_json()
    booking = Cart(order_id=None, booking_id=booking_id, order_datetime=None, rs_quantity=None, price=None, **data)

    try:
        db.session.add(booking)
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
            "data": booking.json()
        }
    ), 201

# Create new room service
@app.route("/cart/add_rs/<string:booking_id>", methods=['POST'])
def create_rs_order(booking_id):
    data = request.get_json()
    booking = Cart(order_id=None, booking_id=booking_id, order_datetime=None, **data)

    try:
        db.session.add(booking)
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
            "data": booking.json()
        }
    ), 201


# Get the number of bookings of a specific facility at a specific timeslot
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)