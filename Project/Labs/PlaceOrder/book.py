from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Book(db.Model):
    __tablename__ = 'book'

    isbn13 = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)

    def __init__(self, isbn13, title, price, availability):
        self.isbn13 = isbn13
        self.title = title
        self.price = price
        self.availability = availability

    def json(self):
        return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}


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


@app.route("/book/<string:isbn13>")
def find_by_isbn13(isbn13):
    book = Book.query.filter_by(isbn13=isbn13).first()
    if book:
        return jsonify(
            {
                "code": 200,
                "data": book.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Book not found."
        }
    ), 404


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
