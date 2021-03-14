from flask import jsonify


class View:
    @staticmethod
    def send_couriers_created(courier_ids):
        """
        HTTP 201 Created
        The method converts the input ids to the JSON-object
        :param courier_ids: a list with numbers (ids of couriers)
        :returns JSON-object with ids of processed couriers
        """
        ids = [{"id": i} for i in courier_ids]
        return jsonify({"couriers": ids})

    @staticmethod
    def send_couriers_bad_request(courier_ids):
        """
        HTTP 400 Bad Request
        The method converts the input ids to the JSON-object with validation error
        :param courier_ids: a list with numbers (ids of couriers)
        :returns JSON-object with validation error and ids of couriers with incorrect data
        """
        ids = [{"id": i} for i in courier_ids]
        return jsonify({"validation_error": {"couriers": ids}})

    @staticmethod
    def send_courier_info(courier):
        """
        HTTP 200 OK
        The method converts the object of type Courier to the JSON-data
        :param courier: the object of type Courier with all information about him
        :return: JSON-object with full information about courier
        """
        return jsonify(courier.__dict__())

    @staticmethod
    def send_courier_full_info(courier):
        """
        HTTP 200 OK
        The method converts the object of type Courier with additional information to the JSON-data
        :param courier: the object of type Courier with all information about him
        :return: JSON-object with full information about courier
        """
        return jsonify(courier.get_data())

    @staticmethod
    def send_orders_created(order_ids):
        """
        HTTP 201 Created
        The method converts the input ids to the JSON-object
        :param order_ids: a list with numbers (ids of orders)
        :returns JSON-object with ids of processed orders
        """
        ids = [{"id": i} for i in order_ids]
        return jsonify({"orders": ids})

    @staticmethod
    def send_orders_bad_request(order_ids):
        """
        HTTP 400 Bad Request
        The method converts the input ids to the JSON-object with validation error
        :param order_ids: a list with numbers (ids of orders)
        :returns JSON-object with validation error and ids of orders with incorrect data
        """
        ids = [{"id": i} for i in order_ids]
        return jsonify({"validation_error": {"orders": ids}})

    @staticmethod
    def send_incorrect_json_bad_request():
        """
        HTTP 400 Bad Request
        The method returns JSON-object with information about parsing error
        :return: JSON-object with validation error and small description of the problem
        """
        return jsonify({"validation_error": {
            "error": 'Syntax error',
            "description": 'Parsing of input JSON is unavailable'
        }})

    @staticmethod
    def send_orders_assign(order_ids, assign_time):
        """
        HTTP 200 OK
        The method converts order ids and assign time of the first request to JSON-object
        :param order_ids: the list of order ids
        :param assign_time: the date of the first order assignment
        :return: JSON-object with given data
        """
        if assign_time is None or len(order_ids) == 0:
            return jsonify({"orders": []})
        ids = [{"id": i} for i in order_ids]
        return jsonify({"orders": ids, "assign_time": assign_time})

    @staticmethod
    def send_order_complete(order_id):
        """
        HTTP 200 OK
        The method returns JSON-object with order id from input
        :param order_id: integer - id of the complete order
        :return: JSON-object with order id
        """
        return jsonify({"order_id": order_id})
