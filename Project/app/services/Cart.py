from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Cart(db.Model):
    __tablename__ = 'Cart'

    OrderID = db.Column(db.Integer, primary_key=True)
    BookingID = db.Column(db.Integer, nullable=False)
    itemID = db.Column(db.Varchar, nullable=False)
    FBDateTime = db.Column(db.DateTime, nullable=False)
    RSQuantity = db.Column(db.Interger, nullable=False)
    Price = db.Column(db.Float(precision=2), nullable=False)


    def __init__(self, OrderID, BookingID, itemID, FBDateTime, RSQuantity, Price):
        self.OrderID = OrderID
        self.BookingID = BookingID
        self.itemID = itemID
        self.FBDateTime = FBDateTime
        self.RSQuantity = RSQuantity
        self.Price = Price
        

    def json(self):
        return {"OrderID": self.OrderID, "BookingID": self.BookingID, "itemID": self.itemID, "FBDateTime": self.FBDateTime, "RSQuantity": self.RSQuantity, "Price": self.Price}

#getting all room service/facility booking request by bookingID
@app.route("/cart/<string:bookingID>")
def get_by_bookingID(bookingID):
    bookings = Cart.query.filter_by(bookingID=bookingID).all()
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

#getting information about a room service/facility booking request by orderID
@app.route("/cart/<string:orderID>")
def get_by_orderID(orderID):
    order = Cart.query.filter_by(orderID=orderID).first()
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

#create new room service/facility booking 
@app.route("/cart/<string:bookingID>", methods=['POST'])
def create_new_booking(bookingID):
    if (Cart.query.filter_by(bookingID=bookingID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "bookingID": bookingID
                },
                "message": "booking already exists."
            }
        ), 400

    data = request.get_json()
    booking = Cart(bookingID, **data)

    try:
        db.session.add(booking)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "bookingID": bookingID
                },
                "message": "An error occurred creating the book."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": booking.json()
        }
    ), 201

#get the number of bookings of a specific facility at a specific timeslot
@app.route("/cart?ItemID=<string:itemID>&FBDateTime=<string:FBDateTime>/")
def get_number_of_bookings(itemID,FBDateTime):
    total = Cart.query.filter_by(itemID=itemID, FBDateTime=FBDateTime).all()
    if len(total):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bookings": [booking.json() for booking in total], #can remove if we just need the total number
                    "total": len(total)
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no bookings."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)