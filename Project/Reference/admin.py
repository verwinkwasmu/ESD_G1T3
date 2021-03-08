from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from os import environ
app = Flask(__name__)

# this is for testing locally
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:8889/admins'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Admin(db.Model):
    __tablename__ = 'admins'

    adminID = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(256), nullable=False)

    def __init__(self, adminID, name, email):
        self.adminID = adminID
        self.name = name
        self.email = email

    def json(self):
        return {"adminID": self.adminID, "name": self.name, "email": self.email}


@app.route('/admin')
def get_all_admin():
    return jsonify({"admins": [admin.json() for admin in Admin.query.all()]})


if __name__ == '__main__':
    # if want to build the image use 0.0.0.0
    # localhost is for testing locally
    # app.run(host='localhost', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
