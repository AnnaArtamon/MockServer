from flask import Flask, request
import json
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    if not path and request.path == '/':
        content_type = request.content_type.split(';')[0]
        if content_type == 'application/json':
            body = request.json
        elif content_type == 'application/xml':
            root = ET.fromstring(request.data)
            body = {child.tag: child.text for child in root}
        else:
            body = request.data.decode('utf-8')
        print(f'Received request with no endpoint specified')
        print(f'Request data: {body}')
        return '', 200

    if path == 'orders' and request.method == 'POST':
        content_type = request.content_type.split(';')[0]
        if content_type == 'application/json':
            body = request.json
            order_id = body.get('order_id')
        elif content_type == 'application/xml':
            root = ET.fromstring(request.data)
            body = {child.tag: child.text for child in root}
            order_id = int(body.get('order_id'))
        else:
            body = request.form
            order_id = int(body.get('order_id'))
        if order_id is None:
            return 'Missing order_id in request body', 400
        if order_id % 2 == 0:
            response = {'accepted': [order_id], 'rejected': []}
        else:
            response = {'accepted': [], 'rejected': [order_id]}
        return json.dumps(response), 200
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp)
    print(f'Received request with URI: {request.url}')
    print(f'Request data: {request.data.decode()}')
    return 'Invalid endpoint', 404

if __name__ == '__main__':
    app.run()
