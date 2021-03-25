from api.__init__ import app, model
from api.handlers.validator import *
from view.view import View


@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    """
    Changes data of a courier with id from input.
    :param courier_id: id of courier who will be changed.
    :return: The result of operation (code 200, 400, or 404).
    """
    try:
        json = validate_and_return_json()
        info = model.patch_courier(courier_id, json)
        return View.send_courier_info(info)
    except WrongCourierData as e:
        return View.send_couriers_bad_request(e.args[0])
    except DataNotFound as e:
        return View.send_couriers_bad_request(e.args[0], code=404)
    except WrongJSONRequest:
        return View.send_incorrect_json_bad_request()
