from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/orders', methods=['POST'])
def orders():
    req_data = request.get_json()

    order_id = req_data['order_id']

    accepted = []
    rejected = []

    if order_id % 2 == 0:
        accepted.append(order_id)
    else:
        rejected.append(order_id)

    response = {
        'accepted': accepted,
        'rejected': rejected
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
