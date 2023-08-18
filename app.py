from flask import Flask, jsonify,request
from main import get_timing


app = Flask(__name__)
@app.route('/')
def home():
    print('go')
    return 'I am alive'

# Sample data
data = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]

@app.route('/flights_api/<flight_number>', methods=['GET'])
def get_items(flight_number):
    print('hi')
    days = int(request.args.get('days', default=7))
    return jsonify(get_timing(flight_number, days))
