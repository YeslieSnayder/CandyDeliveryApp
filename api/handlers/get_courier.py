from api.__init__ import app, model
from api.handlers.validator import *
from view.view import View


@app.route('/couriers/<int:courier_id>', methods=['GET'])
def get_courier(courier_id):
    """
    Returns information of the courier with ID from input.
    :param courier_id: ID of the existing courier.
    Information about the courier with this ID will be included to the response.
    :return: The result of the operation (code 200, 400, or 404) with
    information about the courier with ID from input.
    """
    try:
        courier_data = model.get_courier_full_data(courier_id)
        return View.send_courier_full_info(courier_data)
    except WrongCourierData as e:
        return View.send_couriers_bad_request(e.args[0])
    except DataNotFound as e:
        return View.send_couriers_bad_request(e.args[0], code=404)
