class View:
    @staticmethod
    def send_couriers_created(courier_ids):
        """
        HTTP 201 Created
        :param courier_ids: a list with numbers (ids of couriers)
        :returns an object with ids of processed couriers
        """
        ids = [{"id": i} for i in courier_ids]
        return {"couriers": ids}

    @staticmethod
    def send_couriers_bad_request(courier_ids):
        """
        HTTP 400 Bad Request
        :param courier_ids: a list with numbers (ids of couriers)
        :returns an object with validation error and ids of couriers with incorrect data
        """
        ids = [{"id": i} for i in courier_ids]
        return {"validation_error": {"couriers": ids}}
