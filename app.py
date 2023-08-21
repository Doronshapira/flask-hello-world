from flask import Flask, jsonify, request
from flask_cors import CORS
from main import get_timing
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sslify import SSLify

app = Flask(__name__)
CORS(app, origins=["www.theflightiming.com","https://4a7abb7c-2293-4673-bbd3-7390068b6773.dev.wix-code.com","https://doronsh8.wixstudio.io/my-site-87","https://doronsh8.wixstudio.io"
                  "https://doronsh8.wixstudio.io/","doronsh8.wixstudio.io/my-site-87","doronsh8.wixstudio.io/"], supports_credentials=True)

@app.route('/')
def home():
    print('go')
    return 'I am alive'

@app.route('/flights_api/<flight_number>', methods=['GET'])
def get_items(flight_number):
    days = int(request.args.get('days', default=7))

    response = jsonify(get_timing(flight_number, days))
    
    # Add CORS headers to the response
    response.headers['Access-Control-Allow-Origin'] = 'https://www.theflightiming.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    sslify = SSLify(app, permanent=True)
    app.run(host='0.0.0.0', port=443, ssl_context=('/etc/pki/tls/certs/localhost.crt', '/etc/pki/tls/private/localhost.key'))
