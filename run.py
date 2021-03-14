from flask import Flask, jsonify, request, make_response, abort
from model.model import Model
from view import View
from model.exeptions import *
import re

app = Flask(__name__)
model = Model()


@app.route('/couriers', methods=['POST'])
def post_couriers():
    try:
        if is_incorrect_request() or "data" not in request.get_json():
            return make_response(View.send_couriers_bad_request([]), 400)
        try:
            ids = model.create_couriers(request.get_json()["data"])
            return make_response(View.send_couriers_created(ids), 201)
        except WrongCourierData as e:
            return make_response(View.send_couriers_bad_request(e.args[0]), 400)
    except Exception:
        return make_response(View.send_incorrect_json_bad_request(), 400)


@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    try:
        if is_incorrect_request():
            return make_response(View.send_couriers_bad_request([courier_id]), 400)
        try:
            info = model.patch_courier(courier_id, request.get_json())
            return make_response(View.send_courier_info(info), 200)
        except WrongCourierData as e:
            return make_response(View.send_couriers_bad_request(e.args[0]), 400)
        except DataNotFound as e:
            return make_response(View.send_couriers_bad_request([courier_id]), 404)
    except Exception:
        return make_response(View.send_incorrect_json_bad_request(), 400)


@app.route('/orders', methods=['POST'])
def post_orders():
    try:
        if is_incorrect_request() or "data" not in request.get_json():
            return make_response(View.send_orders_bad_request([]), 400)
        try:
            ids = model.create_orders(request.get_json()["data"])
            return make_response(View.send_orders_created(ids), 201)
        except WrongOrderData as e:
            return make_response(View.send_orders_bad_request(e.args[0]), 400)
    except Exception:
        return make_response(View.send_incorrect_json_bad_request(), 400)


@app.route('/orders/assign', methods=['POST'])
def post_orders_assign():
    try:
        if is_incorrect_request() or "courier_id" not in request.get_json():
            return make_response(View.send_orders_bad_request([]), 400)
        try:
            order_ids, assign_time = model.assign_order(model.get_courier(courier_id=request.get_json()['courier_id']))
            return make_response(View.send_orders_assign(order_ids, assign_time), 200)
        except (WrongOrderData, DataNotFound):
            return make_response(View.send_couriers_bad_request([request.get_json()['courier_id']]), 400)
    except Exception:
        return make_response(View.send_incorrect_json_bad_request(), 400)


@app.route('/orders/complete', methods=['POST'])
def post_orders_complete():
    try:
        if is_incorrect_request():
            return make_response(View.send_orders_bad_request([]), 400)
        json = request.get_json()
        if ("courier_id" or "order_id" or "complete_time") not in json:
            return make_response(View.send_incorrect_json_bad_request(), 400)
        try:
            model.complete_order(json)
            return make_response(View.send_order_complete(json["order_id"]), 200)
        except (DataNotFound, WrongOrderData) as e:
            return make_response(View.send_orders_bad_request(e.args[0]), 400)
        except WrongCourierData as e:
            return make_response(View.send_couriers_bad_request(e.args[0]), 400)
    except Exception:
        return make_response(View.send_incorrect_json_bad_request(), 400)


@app.route('/couriers/<int:courier_id>', methods=['GET'])
def get_courier(courier_id):
    try:
        if is_incorrect_request():
            return make_response(View.send_couriers_bad_request([courier_id]), 400)
        try:
            courier = model.get_courier_full_data(courier_id)
            return make_response(View.send_courier_full_info(courier), 200)
        except WrongCourierData as e:
            return make_response(View.send_couriers_bad_request(e.args[0]), 400)
        except DataNotFound as e:
            return make_response(View.send_couriers_bad_request([courier_id]), 404)
    except Exception:
        return make_response(View.send_incorrect_json_bad_request(), 400)


def is_incorrect_request():
    """
    The method checks the correctness of the entered data.
    Request should be json-type (Content-Type: application/json) and contains at least 1 field.
    :return: True - if request is correct, otherwise - False
    """
    if request is None:
        return True
    if not request.is_json or re.search(r'{.*[\'\"].*[\'\"].*:.*}', request.data.__str__()) is None:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True, port=8080)
