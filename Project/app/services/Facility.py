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

    itemID = db.Column(db.Varchar, primary_key=True)
    itemName = db.Column(db.Varchar, nullable=False)
    Price = db.Column(db.Float(precision=2), nullable=False)
    MaxCapacity = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.Varchar, nullable=False)


    def __init__(self, itemID, itemName, Price, MaxCapacity, Description):
        self.itemID = itemID
        self.itemName = itemName
        self.Price = Price
        self.MaxCapacity = MaxCapacity
        self.Description = Description
        

    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "Price": self.Price, "MaxCapacity": self.MaxCapacity, "Description": self.Description}

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

#getting hotel facility information by itemID
@app.route("/facility/<string:itemID>")
def get_by_itemID(itemID):
    facility = Facility.query.filter_by(itemID=itemID).first()
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