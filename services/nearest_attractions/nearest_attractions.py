
import requests
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.environ.get(
    "GOOGLE_API_KEY") or "AIzaSyAw3Q7eJyqIazB2ucevU3NhnVmsqs5Z3bQ"

@app.route("/nearest_attractions/radius=<int:radius>&type_of_attraction=<string:type_of_attraction>&lat=<float:lat>&lon=<float:lon>")
def get_nearest_attractions(radius, type_of_attraction, lat, lon):

    response = requests.get(
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius={radius}&type={type_of_attraction}&key={GOOGLE_API_KEY}")

    if response.status_code == 200:
        result = response.json()
        return jsonify(
            {
                "code": 200,
                "data": result
            }
        )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Attractions not found."
            }
        ), 404


@app.route("/nearest_attractions/next_page/page_token=<string:page_token>")
def get_next_page(page_token):
    response = requests.get(
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={page_token}&key={GOOGLE_API_KEY}")

    if response.status_code == 200:
        result = response.json()
        return jsonify(
            {
                "code": 200,
                "data": result
            }
        )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Attractions not found."
            }
        ), 404

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5015)) or 5015
    app.run(host="0.0.0.0", port=port, debug=False)
