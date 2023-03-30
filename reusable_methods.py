from flask import Response
import json
import xml.etree.ElementTree as ET

def parse_request_body(content_type: str, data: bytes) -> dict:
    if content_type == 'application/json':
        json_data = json.loads(data)
        return json_data
    elif content_type == 'application/xml':
        root = ET.fromstring(data)
        return {child.tag: child.text for child in root}
    else:
        return {}

def make_response(data, status_code):
    if 'error_message' in data:
        response_data = {'error_message': data['error_message']}
    else:
        response_data = {'data': data}
    response = Response(response=json.dumps(response_data), status=status_code, mimetype='application/json')
    return response
