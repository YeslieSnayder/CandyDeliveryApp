from application.api import app, model
from application.api.handlers.validator import *
from application.view.view import View


@app.route('/orders/complete', methods=['POST'])
def post_orders_complete():
    """
    Makes the order completed.
    :return: The result of the operation (code 200 or 400).
    """
    try:
        json = validate_and_return_json()
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
