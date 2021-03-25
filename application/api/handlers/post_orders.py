from application.api import app, model
from application.api.handlers.validator import *
from application.view.view import View


@app.route('/orders', methods=['POST'])
def post_orders():
    """
    Inserts orders from request to the database.
    :return: The result of the operation (code 201 or 400).
    """
    try:
        json = validate_and_return_json()
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
