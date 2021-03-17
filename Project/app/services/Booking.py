from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

#do i have to write down all columns in db or just the ones i want? 
class Booking(db.Model):
    __tablename__ = 'Booking'

    BookingID = db.Column(db.Integer, primary_key=True)
    GuestName = db.Column(db.String(64), nullable=False)
    NRIC_PassportNO = db.Column(db.Varchar, nullable=False)
    Email = db.Column(db.Varchar, nullable=False)
    StayDuration = db.Column(db.DateTime, nullable=False)
    RoomNumber = db.Column(db.Varchar, nullable=False)
    RoomPrice = db.Column(db.Float(precision=2), nullable=False)
    CheckInStatus = db.Column(db.Boolean, nullable=False)
    CheckOutStatus = db.Column(db.Boolean, nullable=False)

    def __init__(self, BookingID, GuestName, NRIC_PassportNO, Email, StayDuration, RoomNumber, RoomPrice, CheckInStatus, CheckOutStatus ):
        self.BookingID = BookingID
        self.GuestName = GuestName
        self.NRIC_PassportNO = NRIC_PassportNO
        self.Email = Email
        self.StayDuration = StayDuration
        self.RoomNumber = RoomNumber
        self.RoomPrice = RoomPrice
        self.CheckInStatus = CheckInStatus
        self.CheckOutStatus = CheckOutStatus
        

    def json(self):
        return {"BookingID": self.BookingID, "GuestName": self.GuestName, "NRIC_PassportNO": self.NRIC_PassportNO, "Email": self.Email, "StayDuration": self.StayDuration, "RoomNumber": self.RoomNumber, "RoomPrice": self.RoomPrice, "CheckInStatus": self.CheckInStatus, "CheckOutStatus": self.CheckOutStatus}

#getting specific booking with unique BookingID
@app.route("/book/<string:BookingID>")
def find_by_BookingID(BookingID):
    booking = Booking.query.filter_by(BookingID=BookingID).first()
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
