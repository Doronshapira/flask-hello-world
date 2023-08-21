from flask import Flask, jsonify, request
from flask_cors import CORS
from main import get_timing
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sslify import SSLify

app = Flask(__name__)
CORS(app, origins=["https://www.your-wix-app-domain.com"], supports_credentials=True)

@app.route('/')
def home():
    print('go')
    return 'I am alive'

@app.route('/flights_api/<flight_number>', methods=['GET'])
def get_items(flight_number):
    days = int(request.args.get('days', default=7))
    return jsonify(get_timing(flight_number, days))

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    sslify = SSLify(app, permanent=True)
    app.run(host='0.0.0.0', port=443, ssl_context=('/etc/pki/tls/certs/localhost.crt', '/etc/pki/tls/private/localhost.key'))
