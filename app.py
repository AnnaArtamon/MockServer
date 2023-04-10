from flask import Flask, request
import json
from datetime import datetime
from reusable_methods import parse_request_body, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    if not path and request.path == '/':
        content_type = request.content_type.split(';')[0]
        body = parse_request_body(content_type, request.data)
        if body:
            print(f'Received request with no endpoint specified')
            print(f'Request data: {body}')
            return '', 200
        else:
            return make_response({'error_message': 'Invalid request body'}, 400)

    if path == 'orders' and request.method == 'POST':
        content_type = request.content_type.split(';')[0]
        body = parse_request_body(content_type, request.data)
        if isinstance(body, tuple):
            error_message, status_code = body
            return error_message, status_code
        external_id = body[0].get('external_id')
        if external_id is None:
            return make_response({'error_message': 'Missing external_id in request body'}, 400)
        if int(external_id) % 2 == 0:
            response = {'accepted': [external_id], 'rejected': []}
        else:
            response = {'accepted': [], 'rejected': [external_id]}
        return json.dumps(response), 200

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp)
    print(f'Received request with URI: {request.url}')
    print(f'Request data: {request.data.decode()}')
    return make_response({'error_message': 'Invalid endpoint'}, 404)

if __name__ == '__main__':
    context = ('cert.pem', 'key.pem') # replace with the paths to your certificate and private key
    app.run(debug=True, ssl_context=context, host='0.0.0.0', port=8000)