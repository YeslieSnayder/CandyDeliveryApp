import re

from flask import Flask, request, make_response, jsonify

from model.exeptions import *
from model.model import Model
from view import View

app = Flask(__name__)
model = Model()


@app.route('/couriers', methods=['POST'])
def post_couriers():
    try:
        json = check_and_return_json()
        if "data" not in json:
            return View.send_incorrect_json_bad_request()

        ids = model.create_couriers(json["data"])
        return View.send_couriers_created(ids)
    except WrongCourierData as e:
        return View.send_couriers_bad_request(e.args[0])
    except MissingID as e:
        return View.send_error_missing_id(e.args[0], "courier")
    except WrongJSONRequest:
        return View.send_incorrect_json_bad_request()


@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    try:
        json = check_and_return_json()
        info = model.patch_courier(courier_id, json)
        return View.send_courier_info(info)
    except WrongCourierData as e:
        return View.send_couriers_bad_request(e.args[0])
    except DataNotFound as e:
        return View.send_couriers_bad_request(e.args[0], code=404)
    except WrongJSONRequest:
        return View.send_incorrect_json_bad_request()


@app.route('/orders', methods=['POST'])
def post_orders():
    try:
        json = check_and_return_json()
        if "data" not in json:
            return View.send_incorrect_json_bad_request()

        ids = model.create_orders(json["data"])
        return View.send_orders_created(ids)
    except WrongOrderData as e:
        return View.send_orders_bad_request(e.args[0])
    except MissingID as e:
        return View.send_error_missing_id(e.args[0], "order")
    except WrongJSONRequest:
        return View.send_incorrect_json_bad_request()


@app.route('/orders/assign', methods=['POST'])
def post_orders_assign():
    try:
        json = check_and_return_json()
        if "courier_id" not in json:
            return View.send_error_missing_id("No parameter \"courier_id\"", "order")

        order_ids, assign_time = model.assign_order(model.get_courier(courier_id=json['courier_id']))
        return View.send_orders_assign(order_ids, assign_time)
    except (WrongCourierData, DataNotFound) as e:
        return View.send_couriers_bad_request(e.args[0])
    except WrongOrderData as e:
        return View.send_orders_bad_request(e.args[0])
    except WrongJSONRequest:
        return View.send_incorrect_json_bad_request()


@app.route('/orders/complete', methods=['POST'])
def post_orders_complete():
    try:
        json = check_and_return_json()
        if ("courier_id" or "order_id" or "complete_time") not in json:
            return View.send_incorrect_json_bad_request()

        model.complete_order(json)
        return View.send_order_complete(json["order_id"])
    except (DataNotFound, WrongOrderData) as e:
        return View.send_orders_bad_request(e.args[0])
    except WrongCourierData as e:
        return View.send_couriers_bad_request(e.args[0])
    except WrongJSONRequest:
        return View.send_incorrect_json_bad_request()


@app.route('/couriers/<int:courier_id>', methods=['GET'])
def get_courier(courier_id):
    try:
        courier_data = model.get_courier_full_data(courier_id)
        return View.send_courier_full_info(courier_data)
    except WrongCourierData as e:
        return View.send_couriers_bad_request(e.args[0])
    except DataNotFound as e:
        return View.send_couriers_bad_request(e.args[0], code=404)


def check_and_return_json():
    """
    The method checks the correctness of the entered data.
    Request should be json-type (Content-Type: application/json) and contains at least 1 field.
    :return: JSON-object from the request - if the request is correct
    """
    if request is None or not request.is_json \
            or re.search(r'{.*[\'\"].*[\'\"].*:.*}', request.data.__str__()) is None:
        raise WrongJSONRequest
    try:
        return request.get_json()
    except Exception:
        raise WrongJSONRequest()


if __name__ == '__main__':
    app.run(debug=True, port=8080)
