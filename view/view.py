from flask import jsonify, make_response


class View:
    @staticmethod
    def send_couriers_created(courier_ids):
        """
        HTTP 201 Created
        The method converts the input ids to the JSON-object
        and returns a response with the JSON-object.
        :param courier_ids: a list with numbers (ids of couriers).
        :returns a response that contains JSON-object with ids of processed couriers.
        """
        ids = [{"id": i} for i in courier_ids]
        return make_response(jsonify({"couriers": ids}), 201)

    @staticmethod
    def send_couriers_bad_request(courier_ids, code=400):
        """
        HTTP 400 Bad Request | HTTP 404 Not Found
        The method converts the input ids to the JSON-object with validation error
        and returns a response that contains the JSON-object with validation error.
        :param code: a response code.
        :param courier_ids: a list with numbers (ids of couriers).
        :returns a response that contains JSON-object with validation error
        and ids of couriers with incorrect data.
        """
        ids = [{"id": i} for i in courier_ids]
        return make_response(jsonify({"validation_error": {"couriers": ids}}), code)

    @staticmethod
    def send_courier_info(courier):
        """
        HTTP 200 OK
        The method converts the object of type Courier to the JSON-object
        and returns a response contains the JSON-object.
        :param courier: the object of type Courier with all information about him.
        :return: a response that contains JSON-object with given information about courier.
        """
        return make_response(jsonify(courier.__dict__()), 200)

    @staticmethod
    def send_courier_full_info(courier_data):
        """
        HTTP 200 OK
        The method converts dictionary with full information of courier to the JSON-object
        and returns response with the JSON-object.
        :param courier_data: the dictionary with all information about courier.
        :return: a response that contains JSON-object with full information about courier
        """
        return make_response(jsonify(courier_data), 200)

    @staticmethod
    def send_orders_created(order_ids):
        """
        HTTP 201 Created
        The method converts the input ids to the JSON-object
        and returns a response with the JSON-object.
        :param order_ids: a list with numbers (ids of orders).
        :returns a response that contains JSON-object with ids of processed orders.
        """
        ids = [{"id": i} for i in order_ids]
        return make_response(jsonify({"orders": ids}), 201)

    @staticmethod
    def send_orders_bad_request(order_ids, code=400):
        """
        HTTP 400 Bad Request | HTTP 404 Not Found
        The method converts the input ids to the JSON-object with validation error
        and returns response with the JSON-object.
        :param code: a response code.
        :param order_ids: a list with numbers (ids of orders).
        :returns a response that contains JSON-object with validation error
        and ids of orders with incorrect data.
        """
        ids = [{"id": i} for i in order_ids]
        return make_response(jsonify({"validation_error": {"orders": ids}}), code)

    @staticmethod
    def send_incorrect_json_bad_request():
        """
        HTTP 400 Bad Request
        The method returns response contains JSON-object with information about parsing error.
        :return: a response that contains JSON-object with validation error
        and small description of the problem.
        """
        return make_response(jsonify({"validation_error": {
            "error": 'Syntax error',
            "description": 'Parsing of input JSON is unavailable'
        }}), 400)

    @staticmethod
    def send_orders_assign(order_ids, assign_time):
        """
        HTTP 200 OK
        The method converts order ids and assign time of the first request to JSON-object
        and returns corresponding request.
        :param order_ids: the list of order ids.
        :param assign_time: the date of the first order assignment.
        :return: if no assign_time or no order_ids, then the method returns
        a response that contains JSON-object with empty list of orders,
        otherwise, returns a response that contains JSON-object with list of order ids
        and assign time of the order.
        """
        if assign_time is None or len(order_ids) == 0:
            return make_response(jsonify({"orders": []}), 200)
        ids = [{"id": i} for i in order_ids]
        return make_response(jsonify({"orders": ids, "assign_time": assign_time}), 200)

    @staticmethod
    def send_order_complete(order_id):
        """
        HTTP 200 OK
        The method returns response contains JSON-object with order id from input.
        :param order_id: integer - id of the complete order.
        :return: a response that contains JSON-object with order id.
        """
        return make_response(jsonify({"order_id": order_id}), 200)

    @staticmethod
    def send_error_missing_id(message, obj_type):
        """
        HTTP 400 Bad Request
        The method returns response contains JSON-object with information about
        wrong request with missing id of element.
        :param message: Additional message that will send to user.
        :param obj_type: 'courier' or 'order'.
        :return: a response that contains JSON-object with validation error
        and small description of the problem.
        """
        return make_response(jsonify({"validation_error": {
            "error": 'Missing id',
            "object_type": obj_type,
            "description": message
        }}), 400)
