from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bookings'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:8889/bookings'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Booking(db.Model):
    __tablename__ = 'bookings'

    bookingID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.String(2), nullable=True)
    doctorID = db.Column(db.String(2), nullable=False)
    datestart = db.Column(db.DateTime, nullable=True)
    dateend = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    service = db.Column(db.String(256), nullable=True)

    def __init__(self, bookingID, customerID, doctorID, datestart, dateend, status, price, service):
        self.bookingID = bookingID
        self.customerID = customerID
        self.doctorID = doctorID
        self.datestart = datestart
        self.dateend = dateend
        self.status = status
        self.price = price
        self.service = service

    def json(self):
        return {"bookingID": self.bookingID, "customerID": self.customerID, "doctorID": self.doctorID, "datestart": self.datestart, "dateend": self.dateend, "status": self.status, "price": self.price, "service": self.service}


@app.route("/bookings")
def get_all():
    return jsonify({"bookings": [booking.json() for booking in Booking.query.all()]})


@app.route("/bookings/<int:bookingID>")
def find_by_bookingID(bookingID):
    booking = Booking.query.filter_by(bookingID=bookingID).first()
    if booking:
        return jsonify(booking.json())
    return jsonify({"message": "booking ID not found."}), 404


@app.route("/bookings/cid=<string:customerID>")
def find_by_name(customerID):
    booking = Booking.query.filter_by(customerID=customerID).all()
    if booking:
        return jsonify({"bookings": [booking.json() for booking in Booking.query.filter_by(customerID=customerID).all()]})
    return jsonify({"message": "customer ID not found."}), 404


@app.route("/bookings/did=<string:doctorID>")
def find_by_location(doctorID):
    booking = Booking.query.filter_by(doctorID=doctorID).all()
    if booking:
        return jsonify({"bookings": [booking.json() for booking in Booking.query.filter_by(doctorID=doctorID).all()]})
    return jsonify({"message": "doctor ID not found."}), 404


@app.route("/bookings/<int:bookingID>", methods=['POST'])
def create_booking(bookingID):
    if (Booking.query.filter_by(bookingID=bookingID).first()):
        return jsonify({"message": "A booking with bookingID '{}' already exists.".format(bookingID)}), 400

    data = request.get_json()
    booking = Booking(bookingID, **data)

    try:
        db.session.add(booking)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the booking."}), 500

    return jsonify(booking.json()), 201


@app.route("/bookings/<int:bookingID>", methods=['DELETE'])
def delete_booking(bookingID):
    booking = Booking.query.filter_by(
        bookingID=bookingID).first()

    try:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Successfully deleted record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to delete record."}), 500


@app.route("/bookings", methods=['PUT'])
def update_booking():
    data = request.get_json()
    bid = data['bookingID']
    booking = Booking.query.filter_by(
        bookingID=bid).first()
    if(booking):
        if('customerID' in data):
            booking.customerID = data['customerID']
        if('doctorID' in data):
            booking.doctorID = data['doctorID']
        if('datestart' in data):
            booking.datestart = data['datestart']
        if('dateend' in data):
            booking.dateend = data['dateend']
        if('status' in data):
            booking.status = data['status']
        if('price' in data):
            booking.price = data['price']
        if('service' in data):
            booking.service = data['service']

    try:
        db.session.commit()
        return jsonify({"message": "Successfully updated record.", "customerID": booking.customerID}), 200
    except:
        return jsonify({"message": "An error occurred while trying to update record."}), 500


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    # if want to build the image use 0.0.0.0
    # localhost is for testing locally
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
