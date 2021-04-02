from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
#For Mac
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/booking'
#For windows
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/booking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

#do i have to write down all columns in db or just the ones i want? 
class Booking(db.Model):
    __tablename__ = 'Booking'

    booking_id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(64), nullable=False)
    nric_passportno = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    stay_duration = db.Column(db.DateTime, nullable=False)
    room_number = db.Column(db.String, nullable=False)
    room_price = db.Column(db.Float(precision=2), nullable=False)
    discount = db.Column(db.Float(precision=2, nullable=False))
    checkin_status = db.Column(db.Boolean, nullable=False)
    checkout_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, booking_id, guest_name, nric_passportno, email, stay_duration, room_number, room_price, discount, checkin_status, checkout_status ):
        self.booking_id = booking_id
        self.guest_name = guest_name
        self.nric_passportno = nric_passportno
        self.email = email
        self.stay_duration = stay_duration
        self.room_number = room_number
        self.room_price = room_price
        self.discount = discount
        self.checkin_status = checkin_status
        self.checkout_status = checkout_status
        

    def json(self):
        return {"booking_id": self.booking_id, "guest_name": self.guest_name, "nric_passportno": self.nric_passportno, "email": self.email, "stay_duration": self.stay_duration, "room_number": self.room_number, "room_price": self.room_price, "discount": self.discount, "checkin_status": self.checkin_status, "checkout_status": self.checkout_status}

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

# dont think we need to get ALL BOOKINGs right.. since we doing client side of things 
@app.route("/book")
def get_all():
    booklist = Book.query.all()
    if len(booklist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": [book.json() for book in booklist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no books."
        }
    ), 404

#creating bookings is not part of our solution 
@app.route("/book/<string:isbn13>", methods=['POST'])
def create_book(isbn13):
    if (Book.query.filter_by(isbn13=isbn13).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "isbn13": isbn13
                },
                "message": "Book already exists."
            }
        ), 400

    data = request.get_json()
    book = Book(isbn13, **data)

    try:
        db.session.add(book)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "isbn13": isbn13
                },
                "message": "An error occurred creating the book."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": book.json()
        }
    ), 201

# updating information... can consider 
@app.route("/book/<string:isbn13>", methods=['PUT'])
def update_book(isbn13):
    book = Book.query.filter_by(isbn13=isbn13).first()
    if book:
        data = request.get_json()
        if data['title']:
            book.title = data['title']
        if data['price']:
            book.price = data['price']
        if data['availability']:
            book.availability = data['availability'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": book.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "isbn13": isbn13
            },
            "message": "Book not found."
        }
    ), 404

# delete booking is not client side so i never do 
@app.route("/book/<string:isbn13>", methods=['DELETE'])
def delete_book(isbn13):
    book = Book.query.filter_by(isbn13=isbn13).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "isbn13": isbn13
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "isbn13": isbn13
            },
            "message": "Book not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
