from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ 

app = Flask(__name__)
#For Mac
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/booking'

#For windows
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/booking'

# RDS url
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:esdg1t32021@esd-prod.ckcprxmpwut9.us-east-1.rds.amazonaws.com:3306/booking'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

#do i have to write down all columns in db or just the ones i want? 
class Booking(db.Model):
    __tablename__ = 'booking'

    booking_id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(64), nullable=False)
    nric_passportno = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    stay_duration = db.Column(db.DateTime, nullable=False)
    room_number = db.Column(db.String, nullable=False)
    room_price = db.Column(db.Float(precision=2), nullable=False)
    discount = db.Column(db.Float(precision=2), nullable=False)
    checkout_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, booking_id, guest_name, nric_passportno, email, stay_duration, room_number, room_price, discount, checkout_status ):
        self.booking_id = booking_id
        self.guest_name = guest_name
        self.nric_passportno = nric_passportno
        self.email = email
        self.stay_duration = stay_duration
        self.room_number = room_number
        self.room_price = room_price
        self.discount = discount
        self.checkout_status = checkout_status
        

    def json(self):
        return {"booking_id": self.booking_id, "guest_name": self.guest_name, "nric_passportno": self.nric_passportno, "email": self.email, "stay_duration": self.stay_duration, "room_number": self.room_number, "room_price": self.room_price, "discount": self.discount, "checkout_status": self.checkout_status}

#getting specific booking with unique booking_id
@app.route("/booking/<string:booking_id>")
def find_by_booking_id(booking_id):
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if booking:
        return jsonify(
            {
                "code": 200,
                "data": booking.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Booking not found."
        }
    ), 404

# update discount to 10%
# requires booking_id in URL
@app.route("/booking/<string:booking_id>", methods=['PUT'])
def set_discount(booking_id):
    try:
        booking = Booking.query.filter_by(booking_id=booking_id).first()
        if not booking:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "booking_id": booking_id
                    },
                    "message": "booking_id not found."
                }
            ), 404

        # update discount
        booking.discount = 0.1
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": booking.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "booking_id": booking_id
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500

@app.route("/checkout/<string:booking_id>", methods=['PUT'])
def update_checkout(booking_id):
    try:
        booking = Booking.query.filter_by(booking_id=booking_id).first()
        if not booking:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "booking_id": booking_id
                    },
                    "message": "booking_id not found."
                }
            ), 404

        # update discount
        booking.checkout_status = True
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": booking.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "booking_id": booking_id
                },
                "message": "An error occurred while checking out. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host="0.0.0.0",port=port, debug=False)
    
