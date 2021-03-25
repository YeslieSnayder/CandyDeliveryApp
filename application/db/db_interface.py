from application.model.objects import *


class DB:
    def __init__(self):
        """
        Initialization of the database.
        """
        pass

    def create_couriers(self, courier_list: list) -> bool:
        """
        The method imports all couriers from input list to the database.
        :param courier_list: a list that contains objects of type 'Courier'.
        :return: True - creation was successful, otherwise - False.
        """
        pass

    def create_orders(self, order_list: list) -> bool:
        """
        The method imports all orders from input list to the database.
        :param order_list: a list that contains objects of type 'Order'.
        :return: True - creation was successful, otherwise - False.
        """
        pass

    def update_courier(self, courier: Courier) -> bool:
        """
        The method updates data of courier in database by replacing it with new object.
        :param courier: new object of type 'Courier' that will replace the previous
        object in database that has the same id.
        :return: True - updating was successful, otherwise - False
        """
        pass

    def update_order(self, order: Order) -> bool:
        """
        The method updates data of order in database by replacing it with new object.
        :param order: new object of type 'Order' that will replace the previous
        object in database that has the same id.
        :return: True - updating was successful, otherwise - False
        """
        pass

    def get_courier(self, courier_id: int) -> Courier:
        """
        The method returns the object of type 'Courier' that has id from the input.
        :param courier_id: id of courier in database that should be returned.
        :return: if courier with given id exists in the database => the object of type 'Courier'
        otherwise => None
        """
        pass

    def get_order(self, order_id: int) -> Order:
        """
        The method returns the object of type 'Order' that has id from the input.
        :param order_id: id of order in database that should be returned.
        :return: if order with given id exists in the database => the object of type 'Order'
        otherwise => None
        """
        pass

    def get_complete_orders_of_courier(self, courier_id: int) -> list:
        """
        The method returns the list of orders that were completed by courier with id from input.
        :param courier_id: id of a courier that completed the orders.
        :return: the list of orders that were completed by courier with id (courier_id).
        """
        pass

    def get_orders_for_assign(self, courier_payload: int, courier_regions: list) -> list:
        """
        The method returns a list of orders that are satisfied by conditions for assigning.
        It should check the region of order, the weight, delivery time,
        and return the list of the orders.
        :param courier_payload: the maximum payload of the courier.
        :param courier_regions: the regions where courier is working.
        :return: the list with the orders for a courier.
        """
        pass
