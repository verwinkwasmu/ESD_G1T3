
import requests

import os


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


import json

app = Flask(__name__)
CORS(app)


@app.route("/nearest_attractions/radius=<int:radius>&type_of_attraction=<string:type_of_attraction>&lat=<float:lat>&lon=<float:lon>")
def get_nearest_attractions(radius, type_of_attraction, lat, lon):
    GOOGLE_API_KEY = 'AIzaSyAw3Q7eJyqIazB2ucevU3NhnVmsqs5Z3bQ'
    response = requests.get(
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius={radius}&type={type_of_attraction}&key={GOOGLE_API_KEY}&fields=website,rating,place_id,name,formatted_address,formatted_phone_number,photo,price_level,business_status")

    if response.status_code == 200:
        return response.json()
    else:
        return


@app.route("/nearest_attractions/next_page/page_token=<string:page_token>")
def get_next_page(page_token):
    GOOGLE_API_KEY = 'AIzaSyAw3Q7eJyqIazB2ucevU3NhnVmsqs5Z3bQ'
    response = requests.get(
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={page_token}&key={GOOGLE_API_KEY}")

    if response.status_code == 200:
        return response.json()
    else:
        return


if __name__ == "__main__":
    app.run(port=5015, debug=True)