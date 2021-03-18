from model.objects import *


class DB:
    def __init__(self):
        """
        Initialization of the database.
        """
        self.couriers = []
        self.orders = []

    # TODO: Remove after debug
    def get_couriers(self):
        return [i.__dict__() for i in self.couriers]

    # TODO: Remove after debug
    def get_orders(self):
        return [i.__dict__() for i in self.orders]

    def create_couriers(self, courier_list):
        """
        The method imports all couriers from input list to the database.
        :param courier_list: a list that contains objects of type 'Courier'.
        """
        self.couriers = courier_list

    def update_courier(self, courier):
        """
        The method updates data of courier in database by replacing it with new object.
        :param courier: new object of type 'Courier' that will replace the previous
        object in database that has the same id.
        """
        for i in range(len(self.couriers)):
            if self.couriers[i].courier_id == courier.courier_id:
                self.couriers[i] = courier
                break

    def get_courier(self, courier_id):
        """
        The method returns the object of type 'Courier' that has id from the input.
        :param courier_id: id of courier in database that should be returned.
        :return: the object of type 'Courier'
        """
        courier_list = list(filter(lambda courier: courier.courier_id == courier_id, self.couriers))
        if len(courier_list) == 0:
            return None
        return courier_list[0]

    def get_complete_orders_of_courier(self, courier_id):
        """
        The method returns the list of orders that were completed by courier with id from input.
        :param courier_id: id of a courier that completed the orders.
        :return: the list of orders that were completed by courier with id (courier_id).
        """
        return list(filter(lambda courier_temp:
                           courier_temp.courier_id == courier_id and
                           courier_temp.type == Order.TypeOrder.COMPLETE,
                           self.orders))

    def get_order(self, order_id):
        """
        The method returns the object of type 'Order' that has id from the input.
        :param order_id: id of order in database that should be returned.
        :return: the object of type 'Order'
        """
        order_list = list(filter(lambda order: order.order_id == order_id, self.orders))
        if len(order_list) == 0:
            return None
        return order_list[0]

    def create_orders(self, order_list):
        """
        The method imports all orders from input list to the database.
        :param order_list: a list that contains objects of type 'Order'
        :return:
        """
        self.orders = order_list

    def get_orders_for_assign(self, courier_id, courier_payload,
                              courier_regions, courier_working_hours):
        """
        The method returns a list of orders that are satisfied by conditions for assigning.
        It checks the region of order, the weight, delivery time,
        and with deciding knapsack problem it returns the list of the most benefit orders.
        :param courier_id: id of a courier that took the order from previous time.
        :param courier_payload: the maximum payload of the courier.
        :param courier_regions: the regions where courier is working.
        :param courier_working_hours: the working hours of the courier.
        :return: the list with the most benefit orders for a courier.
        """
        return list(filter(lambda order: order.region in courier_regions and
                                         order.weight <= courier_payload and
                                         can_deliver_on_time(order.delivery_hours, courier_working_hours) and
                                         (order.type == Order.TypeOrder.READY or
                                          order.type == Order.TypeOrder.PROCESSING and
                                          order.courier_id == courier_id),
                           self.orders))

    def update_order(self, order: Order):
        """
        The method updates data of order in database by replacing it with new object.
        :param order: new object of type 'Order' that will replace the previous
        object in database that has the same id.
        :return:
        """
        for i in range(len(self.orders)):
            if self.orders[i].order_id == order.order_id:
                self.orders[i] = order
                break


def can_deliver_on_time(delivery_time: list, working_hours: list):
    """
    The method checks the delivery time that should be in boundary of working hours.
    :param delivery_time: delivery time of an order.
    :param working_hours: working hours of a courier.
    :return: True - if delivery time falls under working hours,
    otherwise - False.
    """
    for del_time in delivery_time:
        delivery_start = datetime.strptime(del_time[:5], '%H:%M')
        delivery_end = datetime.strptime(del_time[6:], '%H:%M')

        for work_time in working_hours:
            work_start = datetime.strptime(work_time[:5], '%H:%M')
            work_end = datetime.strptime(work_time[6:], '%H:%M')
            if delivery_start <= work_start < delivery_end or delivery_start < work_end <= delivery_end:
                return True
    return False
