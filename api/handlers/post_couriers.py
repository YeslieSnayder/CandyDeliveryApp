from api.__init__ import app, model
from api.handlers.validator import *
from view.view import View


@app.route('/couriers', methods=['POST'])
def post_couriers():
    """
    Inserts couriers from request to the database.
    :return: The result of operation (code 201 or 400).
    """
    try:
        json = validate_and_return_json()
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
