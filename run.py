from flask import Flask, jsonify, request, make_response, abort
from model.model import Model
from view import View
from model.exeptions import *
import re

app = Flask(__name__)
model = Model()


@app.route('/couriers', methods=['POST'])
def post_couriers():
    if not request.is_json or re.search(r'{.*[\'\"].*[\'\"].*:.*}', request.data.__str__()) is None:
        return make_response(jsonify(View.send_couriers_bad_request([])), 400)
    if request.get_json() is None or "data" not in request.get_json():
        return make_response(jsonify(View.send_couriers_bad_request([])), 400)
    try:
        ids = model.create_couriers(request.get_json()["data"])
        return make_response(jsonify(View.send_couriers_created(ids)), 201)
    except WrongCourierData as e:
        return make_response(jsonify(View.send_couriers_bad_request(e.args[0])), 400)


@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    pass


@app.route('/orders', methods=['POST'])
def post_orders(data):
    pass


@app.route('/orders/assign', methods=['POST'])
def post_orders_assign(data):
    pass


@app.route('/orders/complete', methods=['POST'])
def post_orders_complete(data):
    pass


@app.route('/couriers/<int:courier_id>', methods=['GET'])
def get_courier(courier_id):
    pass


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(error), 400)


if __name__ == '__main__':
    app.run(debug=True)
