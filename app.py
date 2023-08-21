from flask import Flask, jsonify,request
from main import get_timing


app = Flask(__name__)
@app.route('/')
def home():
    print('go')
    return 'I am alive'

@app.route('/flights_api/<flight_number>', methods=['GET'])
def get_items(flight_number):
    days = int(request.args.get('days', default=7))
    return jsonify(get_timing(flight_number, days))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
