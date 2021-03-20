from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/facility'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Facility(db.Model):
    __tablename__ = 'Facility'

    item_id = db.Column(db.Varchar, primary_key=True)
    item_name = db.Column(db.Varchar, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    facility_description = db.Column(db.Varchar, nullable=False)


    def __init__(self, item_id, item_name, price, max_capacity, facility_description):
        self.item_id = item_id
        self.item_name = item_name
        self.price = price
        self.max_capacity = max_capacity
        self.facility_description = facility_description
        

    def json(self):
        return {"item_id": self.item_id, "item_name": self.item_name, "price": self.price, "max_capacity": self.max_capacity, "facility_description": self.facility_description}

#getting all hotel facility information
@app.route("/facility")
def get_all():
    facility_list = Facility.query.all()
    if len(facility_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": [facility.json() for facility in facility_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no facilities."
        }
    ), 404

#getting hotel facility information by item_id
@app.route("/facility/<string:item_id>")
def get_by_item_id(item_id):
    facility = Facility.query.filter_by(item_id=item_id).first()
    if facility:
        return jsonify(
            {
                "code": 200,
                "data": facility.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Facility not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)