from application.api import app, model
from application.api.handlers.validator import *
from application.view.view import View


@app.route('/orders/assign', methods=['POST'])
def post_orders_assign():
    """
    Assigns orders that match the courier's data.
    :return: The result of the operation (code 200 or 400)
    with order IDs corresponding to the courier data.
    """
    try:
        json = validate_and_return_json()
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
